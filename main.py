#!/usr/bin/env python3

import uvicorn
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse, JSONResponse
from pydantic import BaseModel
import turbine_farm
import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('webserver.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)

from config import settings
import bcrypt
import database as local_db

def obtain_session():
  try:
    session = local_db.get_session()
  except Exception as e:
    raise
  return next(session)

session = obtain_session()

def get_session():
  return session
class FilteredUser(BaseModel):
  username: str
  is_admin: bool
  is_flagged: bool

app = FastAPI()

templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'), name='static')

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY.get_secret_value())

@app.post("/login")
async def login(request: Request, session = Depends(get_session)):
  form = await request.form()
  username = form['username'].replace(' ', '').strip()
  password = form['password'].replace(' ', '').strip()
  logger.info(f"User {username} is attempting to log in")
  user_pw_hash = local_db.get_hash_for_user(session, username)
  if user_pw_hash is None:
    logger.info(f"User {username} does not exist")
    return JSONResponse(content={'message': 'Invalid credentials'}, status_code=401)
  if bcrypt.checkpw(password.encode('utf-8'), user_pw_hash):
    logger.info(f"User {username} has successfully logged in")
    request.session['user'] = username
    request.session['is_admin'] = local_db.is_admin(session, username)
    if request.session['is_admin']:
      logger.info(f"User {username} is an admin")
      return JSONResponse(content={'message': 'Successfully logged in', 'redirect': '/admin'}, status_code=200)
    else:
      logger.info(f"User {username} is not an admin")
      return JSONResponse(content={'message': 'Successfully logged in', 'redirect': '/'}, status_code=200)
  logger.info(f"User {username} has failed to log in")
  return JSONResponse(content={'message': 'Invalid credentials'}, status_code=401)

@app.get("/admin")
async def admin(request: Request, session = Depends(get_session)):
  if 'user' in request.session:
    if local_db.is_admin(session, request.session['user']):
      return templates.TemplateResponse('admin_dashboard.html', {'request': request, 'username': request.session['user']})
    else:
      logger.info(f"User {request.session['user']} is not an admin")
      return RedirectResponse(url='/', status_code=303)
  else:
    return RedirectResponse(url='/', status_code=303)

@app.get("/")
async def root(request: Request):
  username = request.session.get('user')
  return templates.TemplateResponse('index.html', {'request': request, 'username': username})

@app.get("/about")
async def get_about(request: Request):
  return templates.TemplateResponse('about.html', {'request': request})

@app.get("/contact")
async def get_contact(request: Request):
  return templates.TemplateResponse('contact.html', {'request': request})

@app.get("/data")
async def get_data(request: Request):
  if 'user' in request.session:
    farm_data = turbine_farm.export_farms_to_json()
    return templates.TemplateResponse('data.html', {'request': request, 'farm_data': farm_data, 'username': request.session['user']})
  return templates.TemplateResponse('data.html', {'request': request, 'farm_data': None, 'username': None})

@app.get("/signout")
async def signout(request: Request):
  request.session.clear()
  return RedirectResponse(url='/', status_code=303)

@app.post("/contact")
async def post_contact(request: Request, session = Depends(get_session)):
  form = await request.form()
  logger.info(f"User {form['name']} has submitted a contact form")
  local_db.create_form(session, form['name'], form['email'], form['phone'], form['message'])
  return JSONResponse(content={'message': 'Form submitted successfully'}, status_code=200)

@app.get("/submissions")
async def get_submissions(request: Request, session = Depends(get_session)):
  if 'user' in request.session:
    if local_db.is_admin(session, request.session['user']):
      logger.info(f"User {request.session['user']} is viewing submissions")
      submissions = local_db.get_forms(session)
      return templates.TemplateResponse('submissions.html', {'request': request, 'submissions': submissions})
    else:
      logger.info(f"User {request.session['user']} is not an admin, and cannot view submissions")
      return RedirectResponse(url='/', status_code=303)
  else:
    return RedirectResponse(url='/', status_code=303)

@app.get("/accounts")
async def get_submissions(request: Request, session = Depends(get_session)):
  if 'user' in request.session:
    if local_db.is_admin(session, request.session['user']):
      logger.info(f"User {request.session['user']} is viewing accounts")
      users = local_db.get_users(session)
      filtered_users: FilteredUser = []
      [filtered_users.append(FilteredUser(username=user.username, is_admin=user.is_admin, is_flagged=user.is_flagged)) for user in users]
      return templates.TemplateResponse('accounts.html', {'request': request, 'accounts': filtered_users})
    else:
      return RedirectResponse(url='/', status_code=303)
  else:
    return RedirectResponse(url='/', status_code=303)

@app.post("/flag/{username}")
async def flag_user(request: Request, username: str, session = Depends(get_session)):
  if 'user' in request.session:
    if local_db.is_admin(session, request.session['user']):
      logger.info(f"User {request.session['user']} is toggling the flag for user {username}")
      is_flagged = local_db.toggle_user_flag(session, username)
      return JSONResponse(content={'message': f"User {username} is {'flagged' if is_flagged else 'unflagged'}"}, status_code=200)
    else:
      return JSONResponse(content={'message': 'Unauthorized'}, status_code=401)
  else:
    return JSONResponse(content={'message': 'Unauthorized'}, status_code=401)

if __name__ == '__main__':
  print("hi bingus!")
  uvicorn.run("main:app", host='127.0.0.1', port=8000)

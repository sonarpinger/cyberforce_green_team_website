#!/usr/bin/env python3

import uvicorn
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse, JSONResponse
from pydantic import BaseModel

from config import settings
import bcrypt
import database as db

def obtain_session():
  try:
    session = db.get_session()
  except Exception as e:
    raise
  return next(session)

class FilteredUser(BaseModel):
  username: str
  is_admin: bool

app = FastAPI()

templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'), name='static')

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY.get_secret_value())

@app.post("/login")
async def login(request: Request, session = Depends(obtain_session)):
  form = await request.form()
  username = form['username']
  password = form['password']
  if bcrypt.checkpw(password.encode('utf-8'), db.get_hash_for_user(session, username)):
    request.session['user'] = username
    return JSONResponse(content={'message': 'Successfully logged in', 'redirect': '/admin'}, status_code=200)
  return JSONResponse(content={'message': 'Invalid credentials'}, status_code=401)

@app.get("/admin")
async def admin(request: Request, session = Depends(obtain_session)):
  if 'user' in request.session:
    if db.is_admin(session, request.session['user']):
      return templates.TemplateResponse('admin_dashboard.html', {'request': request, 'username': request.session['user']})
    else:
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
  return templates.TemplateResponse('data.html', {'request': request})

@app.get("/signout")
async def signout(request: Request):
  request.session.clear()
  return RedirectResponse(url='/', status_code=303)

@app.post("/contact")
async def post_contact(request: Request, session = Depends(obtain_session)):
  form = await request.form()
  db.create_form(session, form['name'], form['email'], form['phone'], form['message'])
  return JSONResponse(content={'message': 'Form submitted successfully'}, status_code=200)

@app.get("/submissions")
async def get_submissions(request: Request, session = Depends(obtain_session)):
  if 'user' in request.session:
    if db.is_admin(session, request.session['user']):
      submissions = db.get_forms(session)
      return templates.TemplateResponse('submissions.html', {'request': request, 'submissions': submissions})
    else:
      return RedirectResponse(url='/', status_code=303)
  else:
    return RedirectResponse(url='/', status_code=303)

@app.get("/accounts")
async def get_submissions(request: Request, session = Depends(obtain_session)):
  if 'user' in request.session:
    if db.is_admin(session, request.session['user']):
      users = db.get_users(session)
      filtered_users: FilteredUser = []
      [filtered_users.append(FilteredUser(username=user.username, is_admin=user.is_admin)) for user in users]
      return templates.TemplateResponse('accounts.html', {'request': request, 'accounts': filtered_users})
    else:
      return RedirectResponse(url='/', status_code=303)
  else:
    return RedirectResponse(url='/', status_code=303)

if __name__ == '__main__':
  print("hi bingus!")
  uvicorn.run("main:app", host='127.0.0.1', port=8000)

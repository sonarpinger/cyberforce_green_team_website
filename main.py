#!/usr/bin/env python3

import uvicorn
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse, JSONResponse

from config import settings
import bcrypt
import database as db

app = FastAPI()

templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'), name='static')

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY.get_secret_value())

@app.post("/login")
async def login(request: Request):
  form = await request.form()
  username = form['username']
  password = form['password']
  hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
  user = db.authenticate_user(db.get_session(), username, hashed_password)
  if user:
    request.session['user'] = username
    return JSONResponse(content={'message': 'Successfully logged in', 'redirect': '/admin'}, status_code=200)
  return JSONResponse(content={'message': 'Invalid credentials'}, status_code=401)

@app.get("/admin")
async def admin(request: Request):
  if 'user' in request.session:
    if db.is_admin(db.get_session(), request.session['user']):
      return templates.TemplateResponse('admin.html', {'request': request})
    else:
      return RedirectResponse(url='/', status_code=303)
  else:
    return RedirectResponse(url='/', status_code=303)

@app.get("/")
async def root(request: Request):
  return templates.TemplateResponse('index.html', {'request': request})

@app.get("/about")
async def get_about(request: Request):
  return templates.TemplateResponse('about.html', {'request': request})

@app.get("/contact")
async def get_contact(request: Request):
  return templates.TemplateResponse('contact.html', {'request': request})

@app.get("/data")
async def get_data(request: Request):
  return templates.TemplateResponse('data.html', {'request': request})

@app.post("/contact")
async def root(request: Request):
  return None

@app.post("/login")
async def login(request: Request):
  form = await request.form()
  username = form['username']
  password = form['password']
  hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
  user = db.authenticate_user(db.get_session(), username, hashed_password)
  if user:
    request.session['user'] = username
    return RedirectResponse(url='/admin', status_code=303)
  return JSONResponse(content={'error': 'Invalid credentials'}, status_code=401)

if __name__ == '__main__':
  print("hi bingus!")
  uvicorn.run("main:app", host='127.0.0.1', port=8000)

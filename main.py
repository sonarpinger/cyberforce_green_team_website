#!/usr/bin/env python3

import uvicorn
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, RedirectResponse

app = FastAPI()

templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'), name='static')

app.add_middleware(SessionMiddleware, secret_key='!secret')

@app.get("/login")
async def login(request: Request):
  return templates.TemplateResponse('login.html', {'request': request})

@app.get("/")
async def root(request: Request):
  return templates.TemplateResponse('index.html', {'request': request})

@app.get("/about")
async def root(request: Request):
  return templates.TemplateResponse('about.html', {'request': request})

@app.get("/contact")
async def root(request: Request):
  return templates.TemplateResponse('contact.html', {'request': request})

@app.post("/contact")
async def root(request: Request):
  return None

@app.post("/login")
async def login(request: Request):
  form = await request.form()
  username = form['username']
  password = form['password']
  if username == 'bingus' and password == 'bingus':
    request.session['user'] = username
    return RedirectResponse(url='/', status_code=303)
  else:
    return RedirectResponse(url='/login', status_code=303)

if __name__ == '__main__':
  print("hi bingus!")
  uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)

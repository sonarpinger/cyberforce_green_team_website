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

if __name__ == '__main__':
  print("hi bingus!")

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from authx import AuthX, AuthXConfig
import uvicorn
import jwt
import asyncio

from html import escape
from urllib.parse import quote, unquote

from database.requests import add_user, chek_user, init_db


app = FastAPI()

templates = Jinja2Templates(directory='app/templates')
app.mount('/app/static', StaticFiles(directory='app/static'), name='static')


config = AuthXConfig()
config.JWT_ACCESS_COOKIE_NAME = 'my_access_cookie'
config.JWT_SECRET_KEY = 'SECRET_KEY'
config.JWT_ALGORITHM = 'HS256'
config.JWT_TOKEN_LOCATION = ['cookies']

security = AuthX(config=config)

class UserSchema(BaseModel):
    username: str
    password: str
    email: str


def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
        return payload
    except Exception as e: print(e)
@app.get('/main', response_class=HTMLResponse)
async def main(request: Request):
    jw_token = request.cookies.get(config.JWT_ACCESS_COOKIE_NAME)
    reg_error_cookie = request.cookies.get('reg_error')
    if reg_error_cookie:
        return templates.TemplateResponse(request=request, name='index.html', context={'reg_error':escape(unquote(reg_error_cookie))})
    if jw_token:
        try:
            username = decode_jwt(token=jw_token)['username']
            return templates.TemplateResponse(request=request, name='index_protected.html', context={'username':username})
        except:
            return templates.TemplateResponse(request=request, name='index.html', context={'reg_error':'Ошибка авторизации'})
    return templates.TemplateResponse(request=request, name='index.html')


@app.post('/registration_user')
async def registration_user(username: str = Form(), email: str = Form(), password: str = Form(), rules_checkbox: bool = Form(False)):
    if username.strip() == '' or password.strip() == '' or email.strip() == '':
        reg_error = 'Заполните все поля'
        response = RedirectResponse(url='/main', status_code=303)
        response.set_cookie(key='reg_error', value=quote(reg_error))
        return response
    
    if not rules_checkbox:
        reg_error = 'Вы не дали свое согласие'
        response = RedirectResponse(url='/main', status_code=303)
        response.set_cookie(key='reg_error', value=quote(reg_error), max_age=5)
        return response
    
    res = await add_user(username=username, password=password, email=email)
    
    if res['registration'] == True:
        jwt = security.create_access_token(uid=username, data={'username':username})
        response = RedirectResponse(url='/main', status_code=303)
        response.set_cookie(key=config.JWT_ACCESS_COOKIE_NAME, value=jwt, max_age=86000)
        response.delete_cookie('reg_error')
        return response
    reg_error = 'Пользователь с таким логином уже зарегестрирован'
    response = RedirectResponse(url='/main', status_code=303)
    response.set_cookie(key='reg_error', value=quote(reg_error), max_age=5)
    return response


@app.post('/login_user', response_class=RedirectResponse)
async def login_user(username: str = Form(), password: str = Form()):
    if username.strip() == '' or password.strip() == '':
        reg_error = 'Заполните все поля'
        response = RedirectResponse(url='/main', status_code=303)
        response.set_cookie(key='reg_error', value=quote(reg_error), max_age=5)
        return response
    res = await chek_user(username=username, password=password)
    
    if res['login'] == True:
        jwt = security.create_access_token(uid=username, data={'username':username})
        response = RedirectResponse(url='/main', status_code=303)
        response.set_cookie(key=config.JWT_ACCESS_COOKIE_NAME, value=jwt, max_age=86000)
        response.delete_cookie('reg_error')
        return response
    reg_error = 'Ошика логина или пароля'
    response = RedirectResponse(url='/main', status_code=303)
    response.set_cookie(key='reg_error', value=quote(reg_error), max_age=5)
    return response


if __name__ == '__main__':
    asyncio.run(init_db())
    uvicorn.run('main:app', reload=True, port=4444)

import hashlib
import io
import logging

import aiohttp
from aiohttp import web

import db_utils.db_request as r

logger = logging.getLogger(__name__)

def hash_pass (password: str) -> str:
    h = hashlib.sha512(password.encode('utf-8'))
    h_pass: str = h.hexdigest()
    return h_pass

async def get_image(request: web.Request):
    imageid: str = request.match_info.get('imageid', '3177c2b93127d51fa22b9e043839e89c')
    img: list = await r.r_image(request.app['db'], imageid)
    ext: str = img[0]['ext']
    content: bytes = img[0]['image']
    return web.Response(body=content, content_type=f'image/{ext}')

async def save_image(request: web.Request):
    post = await request.post()
    ext: str = post.get('ext')
    ext = None if ext not in {'png', 'jpeg'} else ext
    curl: str = post.get('curl')
    curl = None if curl.__len__() != 32 else curl
    image = post.get('image')
    if image:
        img_content: bytes = image.file.read()
        buf: io.BytesIO = io.BytesIO(img_content)
        result = await r.s_aou_image(request.app['db'], buf.getvalue(), ext, curl)
        logger.info(result)
    raise web.HTTPSeeOther(location=f"/admin/img")

async def save_user(request: web.Request):
    post = await request.post()
    login: str = post.get('login')
    t_login: str = None if login.__len__() < 3 else login
    password: str = post.get('password')
    t_password: str = None if password.__len__() < 3 else hash_pass(password)
    new_password: str = post.get('new_password')
    t_new_password: str = None if new_password.__len__() < 3 else hash_pass(new_password)
    if t_login and t_password:
        result = await r.s_aou_auth(request.app['db'], t_login, t_password, t_new_password)
        logger.info(result)
        raise web.HTTPSeeOther(location=f"/user?notify={result}")
    raise web.HTTPSeeOther(location=f"/user?notify=PostRequestError")

async def set_user(request: web.Request):
    post = await request.post()
    login: str = post.get('login')
    t_login: str = None if login.__len__() < 3 else login
    password: str = post.get('password')
    t_password: str = None if password.__len__() < 3 else hash_pass(password)
    if t_login and t_password:
        result = await r.s_set_auth(request.app['db'], t_login, t_password)
        if result not in {'incorrect_login', 'short_password', 'incorrect_login_or_password'}:
            resp: web.Response = web.Response(status=303, headers={'location': '/user?notify=Successfully_completed!'})
            resp.set_cookie(name='user', value=t_login, secure=True)
            resp.set_cookie(name='sid', value=result, secure=True)
            return resp
        else:
            resp: web.Response = web.Response(status=303, headers={'location': f'/user?notify={result}'})
            resp.del_cookie(name='user')
            resp.del_cookie(name='sid')
            logger.info(result)
            return resp
    raise web.HTTPSeeOther(location=f"/user?notify=PostRequestError")
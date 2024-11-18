import hashlib
import io
import logging
import re

from aiohttp import web

import db_utils.db_request as r

logger = logging.getLogger(__name__)
re_gid = re.compile('^([0-9]){3,}$')
re_curl = re.compile('^[a-zA-Z0-9_]{3,64}$')
re_img = re.compile('^[0-9a-f]{32}$')
re_num = re.compile('^([0-9])$')

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
    if request.app['auth'] != 'admin':
        raise web.HTTPSeeOther(location='/?notify=Go+fuck+yourself,+you+bastard!')
    else:
        post = await request.post()
        ext: str = post.get('ext')
        t_ext: str = None if ext not in {'png', 'jpeg'} else ext
        curl: str = post.get('curl')
        t_curl: str = None if curl.__len__() != 32 else curl
        image = post.get('image')
        if image:
            img_content: bytes = image.file.read()
            buf: io.BytesIO = io.BytesIO(img_content)
            result = await r.s_aou_image(request.app['db'], buf.getvalue(), t_ext, t_curl)
            logger.info(result)
            raise web.HTTPSeeOther(location=f"/admin/img?notify={result}")
        raise web.HTTPSeeOther(location=f"/admin/img?notify=PostRequestError")

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

async def save_title(request: web.Request):
    if request.app['auth'] != 'admin':
        raise web.HTTPSeeOther(location='/?notify=Go+fuck+yourself,+you+bastard!')
    else:
        post = await request.post()
        title: str = post.get('title')
        t_title: str = None if title.__len__() < 3 else title
        gid: str = post.get('gid')
        t_gid: int = int(gid) if gid and re_gid.match(gid) else 0
        if t_title:
            result = await r.s_aou_title(request.app['db'], t_title, t_gid)
            logger.info(result)
            raise web.HTTPSeeOther(location=f"/admin?notify={result}")
        raise web.HTTPSeeOther(location=f"/admin?notify=PostRequestError")

async def save_sec(request: web.Request):
    if request.app['auth'] != 'admin':
        raise web.HTTPSeeOther(location='/?notify=Go+fuck+yourself,+you+bastard!')
    else:
        post = await request.post()
        curl: str = post.get('curl')
        t_curl: str = curl if curl and re_curl.match(curl) else None
        priority: str = post.get('priority')
        t_priority: int = int(priority) if priority and re_num.match(priority) else 3
        title: str = post.get('title')
        t_title: str = None if title.__len__() < 3 else title
        adult: str = post.get('adult')
        t_adult: bool = (adult in {'true', 'True', '1'})
        gid: str = post.get('gid')
        t_gid: int = int(gid) if gid and re_gid.match(gid) else 0
        if t_title and t_curl:
            result = await r.s_aou_section(request.app['db'], t_curl, t_priority, t_title, t_adult, t_gid)
            logger.info(result)
            raise web.HTTPSeeOther(location=f"/admin/all?notify={result}")
        raise web.HTTPSeeOther(location=f"/admin/all?notify=PostRequestError")

async def save_chap(request: web.Request):
    if request.app['auth'] != 'admin':
        raise web.HTTPSeeOther(location='/?notify=Go+fuck+yourself,+you+bastard!')
    else:
        post = await request.post()
        curl_sec: str = post.get('curl_sec')
        t_curl_sec: str = curl_sec if curl_sec and re_curl.match(curl_sec) else None
        curl_chap: str = post.get('curl')
        t_curl_chap: str = curl_chap if curl_chap and re_curl.match(curl_chap) else None
        article: str = post.get('article')
        t_article: str = None if article.__len__() < 120 else article
        priority: str = post.get('priority')
        t_priority: int = int(priority) if priority and re_num.match(priority) else 3
        title: str = post.get('title')
        t_title: str = None if title.__len__() < 3 else title
        curl_img_t = post.get('curl_img_t')
        t_curl_img_t: str = curl_img_t if curl_img_t and re_img.match(curl_img_t) else None
        curl_img = post.get('curl_img')
        t_curl_img: str = curl_img if curl_img and re_img.match(curl_img) else None
        center: str = post.get('center_f')
        t_center: bool = (center in {'true', 'True', '1'})
        adult: str = post.get('adult')
        t_adult: bool = (adult in {'true', 'True', '1'})
        gid: str = post.get('gid')
        t_gid: int = int(gid) if gid and re_gid.match(gid) else 0
        if t_curl_sec and t_curl_chap and t_article:
            result = await r.s_aou_chapter(request.app['db'], t_curl_sec, t_curl_chap, t_article
                                           , t_priority, t_title, t_curl_img_t, t_curl_img, t_center
                                           , t_adult, t_gid)
            logger.info(result)
            raise web.HTTPSeeOther(location=f"/admin/{t_curl_sec}/{t_curl_chap}?notify={result}")
        raise web.HTTPSeeOther(location=f"/admin/all/new?notify=PostRequestError")

async def drop(request: web.Request):
    if request.app['auth'] != 'admin':
        raise web.HTTPSeeOther(location='/?notify=Go+fuck+yourself,+you+bastard!')
    else:
        post = await request.post()
        tablename: str = post.get('tablename')
        tablename = None if tablename.__len__() < 3 else tablename
        gid: str = post.get('gid')
        t_gid: int = int(gid) if gid and re_gid.match(gid) else 0
        if tablename:
            result = await r.s_drop(request.app['db'], tablename, t_gid)
            logger.info(result)
            raise web.HTTPSeeOther(location=f"/admin?notify={result}")
        raise web.HTTPSeeOther(location=f"/admin?notify=PostRequestError")
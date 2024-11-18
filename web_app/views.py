import datetime

import aiohttp_jinja2
from aiohttp import web


import db_utils.db_request as r

year: int = datetime.date.today().year

@aiohttp_jinja2.template('index.html')
async def index(request: web.Request):
    sections = await r.r_section(request.app['db'])
    chapters = await r.r_chapter(request.app['db'], None)
    page = await r.r_page(request.app['db'], None, None)
    return {'title': page[0]['title'],
            'adult': page[0]['adult'],
            'curl': page[0]['curl'],
            'auth': request.app['auth'],
            'login': request.app['login'],
            'sections': sections,
            'chapters': chapters,
            'year': year}

@aiohttp_jinja2.template('index.html')
async def section(request: web.Request):
    sec = request.match_info.get('sec', 'all')
    sections = await r.r_section(request.app['db'])
    chapters = await r.r_chapter(request.app['db'], sec)
    page = await r.r_page(request.app['db'], sec, None)
    return {'title': page[0]['title'],
            'adult': page[0]['adult'],
            'curl': page[0]['curl'],
            'auth': request.app['auth'],
            'login': request.app['login'],
            'sections': sections,
            'chapters': chapters,
            'year': year}

@aiohttp_jinja2.template('chapter.html')
async def chapter(request: web.Request):
    sec: str = request.match_info.get('sec')
    chap: str = request.match_info.get('chapter')
    sections = await r.r_section(request.app['db'])
    page = await r.r_page(request.app['db'], sec, chap)
    article = await r.r_article(request.app['db'], sec, chap)
    return {'title': page[0]['title'],
            'adult': page[0]['adult'],
            'curl': page[0]['curl'],
            'auth': request.app['auth'],
            'login': request.app['login'],
            'sections': sections,
            'flg_center': article[0]['flg_center'],
            'imageid': article[0]['imageid'],
            'article': article[0]['article'],
            'year': year}

@aiohttp_jinja2.template('user.html')
async def user(request: web.Request):
    sections = await r.r_section(request.app['db'])
    page = await r.r_page(request.app['db'], None, None)
    return {'title': page[0]['title'],
            'adult': page[0]['adult'],
            'curl': page[0]['curl'],
            'auth': request.app['auth'],
            'login': request.app['login'],
            'sections': sections,
            'year': year}

@aiohttp_jinja2.template('admin.html')
async def admin(request: web.Request):
    sections = await r.r_section(request.app['db'])
    page = await r.r_page(request.app['db'], None, None)
    titles = await r.r_all_title(request.app['db'])
    return {'title': page[0]['title'],
            'adult': page[0]['adult'],
            'curl': page[0]['curl'],
            'auth': request.app['auth'],
            'login': request.app['login'],
            'sections': sections,
            'all_titles': titles,
            'year': year}

@aiohttp_jinja2.template('admin_img.html')
async def admin_img(request: web.Request):
    sections = await r.r_section(request.app['db'])
    all_images = await r.r_all_images(request.app['db'])
    imageid = request.match_info.get('imageid', None)
    page = await r.r_page(request.app['db'], None, None)
    return {'title': page[0]['title'],
            'adult': page[0]['adult'],
            'curl': page[0]['curl'],
            'auth': request.app['auth'],
            'login': request.app['login'],
            'sections': sections,
            'imageid': imageid,
            'all_images': all_images,
            'year': year}

@aiohttp_jinja2.template('admin_sec.html')
async def admin_sec(request: web.Request):
    sec = request.match_info.get('sec')
    sections = await r.r_section(request.app['db'])
    all_sections = await r.r_all_section(request.app['db'])
    page = await r.r_page(request.app['db'], sec, None)
    return {'title': page[0]['title'],
            'adult': page[0]['adult'],
            'curl': page[0]['curl'],
            'auth': request.app['auth'],
            'login': request.app['login'],
            'sections': sections,
            'all_sections': all_sections,
            'year': year}

@aiohttp_jinja2.template('admin_chap.html')
async def admin_chapter(request: web.Request):
    sec: str = request.match_info.get('sec')
    chap: str = request.match_info.get('chapter')
    sections = await r.r_section(request.app['db'])
    raw_article = await r.r_raw_chapter(request.app['db'], sec, chap)
    page = await r.r_page(request.app['db'], sec, chap)
    return {'title': page[0]['title'],
            'adult': page[0]['adult'],
            'curl': page[0]['curl'],
            'auth': request.app['auth'],
            'login': request.app['login'],
            'sections': sections,
            'raw_article': raw_article,
            'year': year}
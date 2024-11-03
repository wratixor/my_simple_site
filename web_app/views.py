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
            'sections': sections,
            'center': article[0]['center'],
            'imageid': article[0]['imageid'],
            'article': article[0]['article'],
            'year': year}

@aiohttp_jinja2.template('admin.html')
async def admin(request: web.Request):
    sections = await r.r_section(request.app['db'])
    page = await r.r_page(request.app['db'], None, None)
    return {'title': page[0]['title'],
            'adult': page[0]['adult'],
            'curl': page[0]['curl'],
            'sections': sections,
            'year': year}
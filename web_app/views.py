import datetime

import aiohttp_jinja2

year: int = datetime.date.today().year

@aiohttp_jinja2.template("index.html")
async def index(request):
    return {'title': 'Wratixor.ru - личный сайт кодера-стихоплюя',
            'year': year}


@aiohttp_jinja2.template("index.html")
async def project(request):
    project_id = request.match_info.get('project', "all")
    return {'title': project_id,
            'year': year}
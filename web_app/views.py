import aiohttp_jinja2

@aiohttp_jinja2.template("index.html")
async def index(request):
    return {'title': 'Тестовая страничка'}


@aiohttp_jinja2.template("index.html")
async def project(request):
    project_id = request.match_info.get('project', "all")
    return {'title': project_id}
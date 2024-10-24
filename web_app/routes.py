import aiohttp

from web_app import views

def setup_routes(app: aiohttp.web.Application):
   app.router.add_static('/static', 'static', append_version=True)
   app.router.add_get("/", views.index)
   app.router.add_get('/{project}', views.project)

import aiohttp

from web_app import views
from web_app import back_utils

def setup_routes(app: aiohttp.web.Application):
   app.router.add_static('/static', 'static', append_version=True)
   app.router.add_get('/img/{imageid}', back_utils.get_image)
   app.router.add_get('/admin', views.admin)
   app.router.add_get('/admin/img/{imageid}', views.admin)
   app.router.add_get('/admin/{sec}', views.admin)
   app.router.add_get('/admin/{sec}/{chapter}', views.admin)
   app.router.add_get('/admin/{sec}/{chapter}', views.admin)
   app.router.add_get('/', views.index)
   app.router.add_get('/{sec}', views.section)
   app.router.add_get('/{sec}/{chapter}', views.chapter)

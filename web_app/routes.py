import aiohttp

from web_app import views
from web_app import back_utils

def setup_routes(app: aiohttp.web.Application):
    app.router.add_static('/static', 'static', append_version=True)
    app.router.add_get('/img/{imageid}', back_utils.get_image)
    app.router.add_get('/user', views.user)
    app.router.add_get('/admin', views.admin)
    app.router.add_get('/admin/img', views.admin_img)
    app.router.add_get('/admin/img/{imageid}', views.admin_img)
    app.router.add_get('/admin/{sec}', views.admin_sec)
    app.router.add_get('/admin/{sec}/{chapter}', views.admin_chapter)
    app.router.add_get('/', views.index)
    app.router.add_get('/{sec}', views.section)
    app.router.add_get('/{sec}/{chapter}', views.chapter)
    app.router.add_post('/admin/img/save', back_utils.save_image)
    app.router.add_post('/admin/title/save', back_utils.save_title)
    app.router.add_post('/admin/sec/save', back_utils.save_sec)
    app.router.add_post('/admin/chapter/save', back_utils.save_chap)
    app.router.add_post('/admin/drop', back_utils.drop)
    app.router.add_post('/user/save', back_utils.save_user)
    app.router.add_post('/user/login', back_utils.set_user)

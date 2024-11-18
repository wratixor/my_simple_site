from typing import Callable, Awaitable

import aiohttp
from aiohttp import web

import db_utils.db_request as r


@web.middleware
async def auth_middleware(request: web.Request, handler: Callable[[web.Request], Awaitable[web.Response]]):
    login: str = request.cookies.get('user')
    sid: str = request.cookies.get('sid')
    result: str = await r.s_get_auth(request.app['db'], login, sid)
    if result not in {'user', 'admin', 'anon'}:
        request.app['auth'] = None
        request.app['login'] = None
        resp: web.Response = web.Response(status=303, headers={'location': f'/user?notify={result}'})
        resp.del_cookie(name='user')
        resp.del_cookie(name='sid')
        return resp
    else:
        request.app['auth'] = result
        request.app['login'] = login
        return await handler(request)

def setup_middlewares(app: aiohttp.web.Application):
    app.middlewares.append(auth_middleware)
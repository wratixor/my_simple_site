import logging
import ssl

import aiohttp
import aiohttp_jinja2
import jinja2
from aiohttp import web
from decouple import config

from db_utils.db_class import DB
from web_app import routes
from web_app import middlewares

logging.basicConfig(level=logging.CRITICAL, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_app() -> web.Application:
    web_app = web.Application()

    middlewares.setup_middlewares(web_app)
    routes.setup_routes(web_app)
    aiohttp_jinja2.setup(web_app, loader=jinja2.FileSystemLoader('template'))

    cert: str or None = None
    key: str or None = None
    try:
        cert = config('CERT')
        key = config('KEY')
    except Exception as e:
        logger.error(e)

    if cert and key:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(cert, key)
    else:
        ssl_context = None

    web_app['ssl']: ssl.SSLContext = ssl_context
    web_app['host']: str = config('HOST')
    web_app['port']: int = int(config('PORT'))
    web_app['pg']: str = config('PG_LINK')
    web_app['db']: DB = DB()
    web_app['db'].setup(web_app)
    return web_app

if __name__ == '__main__':
    app = create_app()
    aiohttp.web.run_app(app=app, host=app['host'], port=app['port']
                        , ssl_context=app['ssl'], handler_cancellation=True)
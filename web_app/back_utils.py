import io
import logging

from aiohttp import web

import db_utils.db_request as r

logger = logging.getLogger(__name__)


async def get_image(request: web.Request):
    imageid: str = request.match_info.get('imageid', '3177c2b93127d51fa22b9e043839e89c')
    img: list = await r.r_image(request.app['db'], imageid)
    ext: str = img[0]['ext']
    content: bytes = img[0]['image']
    return web.Response(body=content, content_type=f'image/{ext}')

async def save_image(request: web.Request):
    post = await request.post()
    ext: str = post.get('ext')
    ext = None if ext not in {'png', 'jpeg'} else ext
    curl: str = post.get('curl')
    curl = None if curl.__len__() != 32 else curl
    image = post.get('image')
    if image:
        img_content: bytes = image.file.read()
        buf: io.BytesIO = io.BytesIO(img_content)
        result = await r.s_aou_image(request.app['db'], buf.getvalue(), ext, curl)
        logger.info(result)
    raise web.HTTPSeeOther(location=f"/admin/img")
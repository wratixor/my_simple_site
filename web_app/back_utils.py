import io

import PIL
import PIL.Image
from PIL.Image import Image
from aiohttp import web

import db_utils.db_request as r

async def get_image(request: web.Request):
    imageid: str = request.match_info.get('imageid', 'default')
    img: Image
    if imageid == 'thumb':
        img = PIL.Image.new('RGB', (200, 200), color='#ff0000')
    elif imageid == 'desc':
        img = PIL.Image.new('RGB', (640, 360), color='#00ff00')
    else:
        img = PIL.Image.new('RGB', (36, 36), color='#0000ff')
    fp = io.BytesIO()
    img.save(fp, format='PNG')
    content = fp.getvalue()
    return web.Response(body=content, content_type="image/png")
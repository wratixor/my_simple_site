import io

import PIL
import PIL.Image
from PIL.Image import Image
from aiohttp import web

import db_utils.db_request as r

async def get_image(request: web.Request):
    imageid: str = '5f74613cded5a111c2f4975a4f6ea091' #request.match_info.get('imageid', 'b86ec832a8503110c5d716896816e176')
    img: list = await r.r_image(request.app['db'], imageid)
    ext: str = img[0]['ext']
    content = img[0]['image']
    return web.Response(body=content, content_type=f'image/{ext}')
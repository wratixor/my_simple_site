import datetime
import logging
from asyncpg import Record

from db_utils.db_class import DB

logger = logging.getLogger(__name__)


async def r_section(db: DB) -> list[Record]:
    pool = await db.get_pool()
    result: list[Record]
    async with pool.acquire() as conn:
        try:
            result = await conn.fetch('select * from api.r_section()')
        except Exception as e:
            logger.error(f'Exception r_section(): {e}')
    return result

async def r_chapter(db: DB, section: str = None) -> list[Record]:
    pool = await db.get_pool()
    result: list[Record]
    async with pool.acquire() as conn:
        try:
            result = await conn.fetch('select * from api.r_all_chapter($1::text)', section)
        except Exception as e:
            logger.error(f'Exception r_all_chapter({section}): {e}')
    return result

async def r_article(db: DB, section: str = None, chapter: str = None) -> list[Record]:
    pool = await db.get_pool()
    result: list[Record]
    async with pool.acquire() as conn:
        try:
            result = await conn.fetch('select * from api.r_chapter($1::text)', chapter)
        except Exception as e:
            logger.error(f'Exception r_chapter({chapter}): {e}')
    return result

async def r_page(db: DB, section: str = None, chapter: str = None) -> list[Record]:
    pool = await db.get_pool()
    result: list[Record]
    async with pool.acquire() as conn:
        try:
            result = await conn.fetch('select * from api.r_page($1::text, $2::text)', section, chapter)
        except Exception as e:
            logger.error(f'Exception r_page({section}, {chapter}): {e}')
    return result

async def r_image(db: DB, imgid: str = None) -> list[Record]:
    pool = await db.get_pool()
    result: list[Record]
    async with pool.acquire() as conn:
        try:
            result = await conn.fetch('select * from api.r_image($1::text)', imgid)
        except Exception as e:
            logger.error(f'Exception r_image({imgid}): {e}')
    return result

async def s_aou_auth(db: DB, login: str = None, password: str = None, new_password: str = None) -> str:
    pool = await db.get_pool()
    result: str
    async with pool.acquire() as conn:
        try:
            result = await conn.fetchval('select * from api.s_aou_auth($1::text, $2::text, $3::text)', login, password, new_password)
        except Exception as e:
            result = f'Exception s_aou_auth({login}, {password}, {new_password}): {e}'
            logger.error(result)
    return result

async def s_set_auth(db: DB, login: str = None, password: str = None) -> str:
    pool = await db.get_pool()
    result: str
    async with pool.acquire() as conn:
        try:
            result = await conn.fetchval('select * from api.s_set_auth($1::text, $2::text)', login, password)
        except Exception as e:
            result = f'Exception s_set_auth({login}, {password}): {e}'
            logger.error(result)
    return result

async def s_get_auth(db: DB, login: str = None, sid: str = None) -> str:
    pool = await db.get_pool()
    result: str
    async with pool.acquire() as conn:
        try:
            result = await conn.fetchval('select * from api.s_get_auth($1::text, $2::text)', login, sid)
        except Exception as e:
            result = f'Exception s_get_auth({login}, {sid}): {e}'
            logger.error(result)
    return result

async def r_all_images(db: DB) -> list[Record]:
    pool = await db.get_pool()
    result: list[Record]
    async with pool.acquire() as conn:
        try:
            result = await conn.fetch('select * from api.r_all_images()')
        except Exception as e:
            logger.error(f'Exception r_all_images(=): {e}')
    return result

async def s_aou_image(db: DB, image: bytes, ext: str = None, curl: str = None) -> str:
    pool = await db.get_pool()
    result: str
    async with pool.acquire() as conn:
        try:
            result = await conn.fetchval('select * from api.s_aou_image($1::bytea, $2::text, $3::text)', image, ext, curl)
        except Exception as e:
            result = f'Exception s_aou_image({image}, {ext}, {curl}): {e}'
            logger.error(result)
    return result

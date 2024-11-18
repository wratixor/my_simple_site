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

async def r_raw_chapter(db: DB, section: str = None, chapter: str = None) -> list[Record]:
    pool = await db.get_pool()
    result: list[Record]
    async with pool.acquire() as conn:
        try:
            result = await conn.fetch('select * from api.r_raw_chapter($1::text)', chapter)
        except Exception as e:
            logger.error(f'Exception r_raw_chapter({chapter}): {e}')
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
            result = await conn.fetchval('select * from api.s_aou_auth'
                                         '($1::text, $2::text, $3::text)'
                                         , login, password, new_password)
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
            logger.error(f'Exception r_all_images(): {e}')
    return result

async def s_aou_image(db: DB, image: bytes, ext: str = None, curl: str = None) -> str:
    pool = await db.get_pool()
    result: str
    async with pool.acquire() as conn:
        try:
            result = await conn.fetchval('select * from api.s_aou_image'
                                         '($1::bytea, $2::text, $3::text)'
                                         , image, ext, curl)
        except Exception as e:
            result = f'Exception s_aou_image({image}, {ext}, {curl}): {e}'
            logger.error(result)
    return result

async def r_all_title(db: DB) -> list[Record]:
    pool = await db.get_pool()
    result: list[Record]
    async with pool.acquire() as conn:
        try:
            result = await conn.fetch('select * from api.r_all_title()')
        except Exception as e:
            logger.error(f'Exception r_all_title(): {e}')
    return result

async def s_aou_title(db: DB, title: str, gid: int = None) -> str:
    pool = await db.get_pool()
    result: str
    async with pool.acquire() as conn:
        try:
            result = await conn.fetchval('select * from api.s_aou_title($1::text, $2::bigint)', title, gid)
        except Exception as e:
            result = f'Exception s_aou_title({title}, {gid}): {e}'
            logger.error(result)
    return result

async def r_all_section(db: DB) -> list[Record]:
    pool = await db.get_pool()
    result: list[Record]
    async with pool.acquire() as conn:
        try:
            result = await conn.fetch('select * from api.r_all_section()')
        except Exception as e:
            logger.error(f'Exception r_all_section(): {e}')
    return result

async def s_aou_section(db: DB, curl: str, priority: int, title: str, adult: bool, gid: int = None) -> str:
    pool = await db.get_pool()
    result: str
    async with pool.acquire() as conn:
        try:
            result = await conn.fetchval('select * from api.s_aou_section'
                                         '($1::text, $2::int, $3::text, $4::boolean, $5::bigint)'
                                         , curl, priority, title, adult, gid)
        except Exception as e:
            result = f'Exception s_aou_section({curl}, {priority}, {title}, {adult}, {gid}): {e}'
            logger.error(result)
    return result

async def s_aou_chapter(db: DB, curl_sec: str, curl_chap: str, article: str, priority: int, title: str
                        , curl_img_t: str = None, curl_img: str = None, center: bool = None
                        , adult: bool = None, gid: int = None) -> str:
    pool = await db.get_pool()
    result: str
    async with pool.acquire() as conn:
        try:
            result = await conn.fetchval('select * from api.s_aou_chapter'
                                         '($1::text, $2::text, $3::text, $4::int, $5::text, $6::text, $7::text'
                                         ', $8::boolean, $9::boolean, $10::bigint)'
                                         , curl_sec, curl_chap, article, priority, title, curl_img_t, curl_img
                                         , center, adult, gid)
        except Exception as e:
            result = (f'Exception s_aou_chapter({curl_sec}, {curl_chap}, %article%, {priority}, {title}'
                      f', {curl_img_t}, {curl_img}, {center}, {adult}, {gid}): {e}')
            logger.error(result)
    return result

async def s_drop(db: DB, tablename: str, gid: int = None) -> str:
    pool = await db.get_pool()
    result: str
    async with pool.acquire() as conn:
        try:
            result = await conn.fetchval('select * from api.s_drop ($1::text, $2::bigint)', tablename, gid)
        except Exception as e:
            result = f'Exception s_drop({tablename}, {gid}): {e}'
            logger.error(result)
    return result
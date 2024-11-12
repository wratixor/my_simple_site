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


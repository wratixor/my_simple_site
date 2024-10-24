import datetime
import logging
from asyncpg import Record

from db_utils.db_class import DB

logger = logging.getLogger(__name__)

async def s_name_join(db: DB, user_id: int, group_id: int, username: str) -> str:
    pool = await db.get_pool()
    result: str
    async with pool.acquire() as conn:
        try:
            result = await conn.fetchval("select * from api.s_name_join($1::bigint, $2::bigint, $3::text)"
                                         , user_id, group_id, username)
        except Exception as e:
            result = f"Exception s_name_join({user_id}, {group_id}, {username}): {e}"
            logger.error(result)
    return result

async def s_upd_vacation(db: DB, user_id: int, vacation_gid: int
                       , date_begin: datetime.date = None, date_end: datetime.date = None, day_count: int = None) -> str:
    pool = await db.get_pool()
    result: str
    async with pool.acquire() as conn:
        try:
            result = await conn.fetchval("select * from api.s_upd_vacation($1::bigint, $2::bigint, $3::date, $4::date, $5::integer)"
                                         , user_id, vacation_gid, date_begin, date_end, day_count)
        except Exception as e:
            result = f"Exception s_upd_vacation({user_id}, {vacation_gid}, {date_begin}, {date_end}, {day_count}) exception: {e}"
            logger.error(result)
    return result

async def r_myvacation(db: DB, user_id: int, n_year: int = None) -> list[Record]:
    pool = await db.get_pool()
    result: list[Record]
    async with pool.acquire() as conn:
        try:
            result = await conn.fetch("select * from api.r_myvacation($1::bigint, $2::integer)"
                                         , user_id, n_year)
        except Exception as e:
            logger.error(f"Exception r_myvacation({user_id}, {n_year}): {e}")
    return result
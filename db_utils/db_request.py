import datetime
import logging
from asyncpg import Record

from db_utils.db_class import DB

logger = logging.getLogger(__name__)


async def r_section(db: DB) -> list[Record]:
    # pool = await db.get_pool()
    # result: list[Record]
    # async with pool.acquire() as conn:
    #     try:
    #         result = await conn.fetch('select * from api.r_section()')
    #     except Exception as e:
    #         logger.error(f'Exception r_section(): {e}')
    result: list = [{'curl': 'section-1', 'title': 'Раздел 1'},
                    {'curl': 'section-2', 'title': 'Раздел 2'},
                    {'curl': 'section-3', 'title': 'Раздел 3'},
                    {'curl': 'section-4', 'title': 'Раздел 4'},
                    {'curl': 'section-5', 'title': 'Раздел 5'}]
    return result

async def r_chapter(db: DB, section: str = None) -> list[Record]:
    if section in {'/all', '', None}:
        section = 'glagne'
    defaultitem: str = f'''
    <i>{datetime.datetime.now().strftime('%d.%m.%Y, %H:%M:%S')}</i> <b>{section.upper()}:</b><br/>
    Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet
    Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet Lorem ipsum dolor sit amet
    '''
    # pool = await db.get_pool()
    # result: list[Record]
    # async with pool.acquire() as conn:
    #     try:
    #         result = await conn.fetch('select * from api.r_chapter($1::text)', section)
    #     except Exception as e:
    #         logger.error(f'Exception r_chapter({section}): {e}')
    result: list = [{'curl': f'{section}/chapter-1', 'imageid': 'thumb', 'item': defaultitem},
                    {'curl': f'{section}/chapter-2', 'imageid': 'thumb', 'item': defaultitem},
                    {'curl': f'{section}/chapter-3', 'imageid': 'thumb', 'item': defaultitem},
                    {'curl': f'{section}/chapter-4', 'imageid': 'thumb', 'item': defaultitem},
                    {'curl': f'{section}/chapter-5', 'imageid': 'thumb', 'item': defaultitem}]
    return result

async def r_article(db: DB, section: str = None, chapter: str = None) -> list[Record]:
    a: int = 1 if section == 'section-4' else 0
    defaultitem: str = f'''
        <h3>{section} : {chapter}</h3>
        <i>Lorem ipsum dolor sit amet lorem ipsum dolor sit amet Lorem ipsum dolor sit amet lorem ipsum dolor</i><br/>
        <code>Lorem ipsum dolor sit amet lorem ipsum dolor sit amet Lorem ipsum dolor sit amet lorem ipsum dolor</code><br/>
        <p>
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet Lorem ipsum dolor sit amet lorem ipsum dolor
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet Lorem ipsum dolor sit amet lorem ipsum dolor
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet Lorem ipsum dolor sit amet lorem ipsum dolor
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet Lorem ipsum dolor sit amet lorem ipsum dolor
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet Lorem ipsum dolor sit amet lorem ipsum dolor
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet Lorem ipsum dolor sit amet lorem ipsum dolor
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet Lorem ipsum dolor sit amet lorem ipsum dolor
        </p>
        <p>
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet Lorem ipsum dolor sit amet lorem ipsum dolor
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet Lorem ipsum dolor sit amet lorem ipsum dolor
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet Lorem ipsum dolor sit amet lorem ipsum dolor
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet Lorem ipsum dolor sit amet lorem ipsum dolor
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet Lorem ipsum dolor sit amet lorem ipsum dolor
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet Lorem ipsum dolor sit amet lorem ipsum dolor
            Lorem ipsum dolor sit amet lorem ipsum dolor sit amet Lorem ipsum dolor sit amet lorem ipsum dolor
        </p>
        <br/><br/><br/>
        <i>{datetime.datetime.now().strftime('%d.%m.%Y, %H:%M:%S')}</i>
        <br/>
        '''
    # pool = await db.get_pool()
    # result: list[Record]
    # async with pool.acquire() as conn:
    #     try:
    #         result = await conn.fetch('select * from api.r_article($1::text, $2::text)', section, chapter)
    #     except Exception as e:
    #         logger.error(f'Exception r_article({section}, {chapter}): {e}')
    result: list = [{'center': a, 'imageid': 'desc', 'article': defaultitem}]
    return result

async def r_page(db: DB, section: str = None, chapter: str = None) -> list[Record]:
    a: int = 1 if section == 'section-4' else 0
    title: str = ((f'{section}: ' if section else 'Wratixor.ru - ')
                  + (f'{chapter}' if chapter else 'Личный сайт кодера-стихоплюя'))
    # pool = await db.get_pool()
    # result: list[Record]
    # async with pool.acquire() as conn:
    #     try:
    #         result = await conn.fetch('select * from api.r_page($1::text, $2::text)', section, chapter)
    #     except Exception as e:
    #         logger.error(f'Exception r_page({section}, {chapter}): {e}')
    result: list = [{'adult': a, 'title': f'{title}'}]
    return result


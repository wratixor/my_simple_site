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
    <i>{datetime.datetime.now().strftime('%d.%m.%Y, %H:%M:%S')}</i><br/>
    <b>{section.upper()}:</b><br/>
    Lorem ipsum dolor sit amet 1 Lorem ipsum dolor sit amet 2 Lorem ipsum dolor sit amet 3 Lorem ipsum dolor sit amet 4
    Lorem ipsum dolor sit amet 5 Lorem ipsum dolor sit amet 6 Lorem ipsum dolor sit amet 7 Lorem ipsum dolor sit amet 8
    '''
    # pool = await db.get_pool()
    # result: list[Record]
    # async with pool.acquire() as conn:
    #     try:
    #         result = await conn.fetch('select * from api.r_all_chapter($1::text)', section)
    #     except Exception as e:
    #         logger.error(f'Exception r_all_chapter({section}): {e}')
    result: list = [{'curl': f'{section}/chapter-1', 'imageid': 'thumb', 'item': defaultitem},
                    {'curl': f'{section}/chapter-2', 'imageid': 'thumb', 'item': defaultitem},
                    {'curl': f'{section}/chapter-3', 'imageid': 'thumb', 'item': defaultitem},
                    {'curl': f'{section}/chapter-4', 'imageid': 'thumb', 'item': defaultitem},
                    {'curl': f'{section}/chapter-5', 'imageid': 'thumb', 'item': defaultitem}]
    return result

async def r_article(db: DB, section: str = None, chapter: str = None) -> list[Record]:
    a: bool = section == 'section-4'
    defaultitem: str = f'''
        <h3>{section} : {chapter}</h3>
        <p>
            Lorem ipsum dolor sit amet<br/>
            lorem ipsum dolor sit amet<br/>
            Lorem ipsum dolor sit amet<br/>
            lorem ipsum dolor sit amet
        </p>
        <p>
            Lorem ipsum dolor sit amet<br/>
            lorem ipsum dolor sit amet<br/>
            Lorem ipsum dolor sit amet<br/>
            lorem ipsum dolor sit amet
        </p>
        <p>
            Lorem ipsum dolor sit amet<br/>
            lorem ipsum dolor sit amet<br/>
            Lorem ipsum dolor sit amet<br/>
            lorem ipsum dolor sit amet
        </p>
        <p>
            Lorem ipsum dolor sit amet<br/>
            lorem ipsum dolor sit amet<br/>
            Lorem ipsum dolor sit amet<br/>
            lorem ipsum dolor sit amet
        </p>
        <br/><br/><br/>
        <i>{datetime.datetime.now().strftime('%d.%m.%Y, %H:%M:%S')}</i>
        <br/>
        '''
    # pool = await db.get_pool()
    # result: list[Record]
    # async with pool.acquire() as conn:
    #     try:
    #         result = await conn.fetch('select * from api.r_chapter($1::text, $2::text)', section, chapter)
    #     except Exception as e:
    #         logger.error(f'Exception r_chapter({section}, {chapter}): {e}')
    result: list = [{'flg_center': a, 'imageid': 'desc' if not a else '', 'article': defaultitem}]
    return result

async def r_page(db: DB, section: str = None, chapter: str = None) -> list[Record]:
    a: bool =  section == 'section-4'
    title: str = ((f'{section}: ' if section else 'Wratixor.ru - ')
                  + (f'{chapter}' if chapter else 'Личный сайт кодера-стихоплюя'))
    curl: str = (f'/{section}' if section else '') + (f'/{chapter}' if chapter else '')
    # pool = await db.get_pool()
    # result: list[Record]
    # async with pool.acquire() as conn:
    #     try:
    #         result = await conn.fetch('select * from api.r_page($1::text, $2::text)', section, chapter)
    #     except Exception as e:
    #         logger.error(f'Exception r_page({section}, {chapter}): {e}')
    result: list = [{'adult': a, 'title': title, 'curl': curl}]
    return result


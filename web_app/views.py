import datetime

import aiohttp_jinja2

year: int = datetime.date.today().year

@aiohttp_jinja2.template("index.html")
async def index(request):
    return {'title': 'Wratixor.ru - личный сайт кодера-стихоплюя',
            'year': year}

@aiohttp_jinja2.template("index.html")
async def section(request):
    title = request.match_info.get('sec', "all")
    center: int = (int(request.match_info.get('sec')[-1:]) % 2)
    return {'title': title,
            'adult': center,
            'year': year}

@aiohttp_jinja2.template("chapter.html")
async def chapter(request):
    title: str = f'{request.match_info.get('sec')}: {request.match_info.get('chapter')}'
    center: int = (int(request.match_info.get('chapter')[-1:]) % 2)
    img: str = ''
    if center == 0:
        img = 'description_bot.png'
    article: str = '''
    <p><b>Lorem ipsum dolor sit amet lorem ipsum dolor sit amet</b></p>
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
    '''
    return {'title': title,
            'adult': center,
            'center': center,
            'descimg': img,
            'article': article,
            'year': year}

@aiohttp_jinja2.template("admin.html")
async def admin(request):

    return {'title': 'Админка',
            'year': year}
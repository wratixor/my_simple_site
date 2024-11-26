<H1>My simple site</H1>
<h2>For https://wratixor.ru</h2>

<h3>Requirements:</h3>
 - python-decouple<br>
 - asyncpg<br>
 - aiohttp<br>
 - aiohttp-jinja2<br>
 - jinja2<br>

<h3>Install:</h3>
- <code>git clone https://github.com/wratixor/my_simple_site</code><br>
- <code>python3 -m venv .venv</code><br>
- <code>source .venv/bin/activate</code><br>
- <code>pip install -r requirements.txt</code><br>
- Edit template.env and rename to .env<br>
- Create postgres db and schemas "api" and "rmaster"<br>
- Run <code>./db_utils/init_db.sql</code> in psql<br>
- Edit site.service<br>
- <code>ln -s /../site.service /etc/systemd/system</code><br>
- <code>systemctl enable site.service</code><br>
- <code>systemctl start site.service</code><br>



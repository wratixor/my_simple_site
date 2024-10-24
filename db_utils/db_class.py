import asyncpg
from aiohttp import web


class DB:

    def __init__(self):
        self.config: str or None = None
        self._pool: asyncpg.pool.Pool or None = None

    async def get_pool(self) -> asyncpg.pool.Pool:
        return self._pool

    def setup(self, application: web.Application) -> None:
        application.on_startup.append(self._on_connect)
        application.on_cleanup.append(self._on_disconnect)

    async def _on_connect(self, application: web.Application):
        self.config = application['pg']
        self._pool = await asyncpg.create_pool(dsn=self.config)

    async def _on_disconnect(self, _) -> None:
        if self._pool is not None:
            await self._pool.close()
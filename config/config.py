import os
from dotenv import load_dotenv


class Config:
    def __init__(self) -> None:
        load_dotenv()

        self._BOT_API = os.getenv('BOT_API')

        if not self._BOT_API:
            print('Не получен бота апи')

        self.DB_NAME = os.getenv("DB_NAME", 'root')
        self.DB_USER = os.getenv("DB_USER", 'root')
        self.DB_PASS = os.getenv("DB_PASS", "root")
        self.DB_PORT = os.getenv("DB_PORT", 5432)

        self._DEBUG = os.getenv("DEBUG", False)

    async def get_database_link(self):
        return f''

    async def get_bot_api(self):
        return self._BOT_API

    async def get_debug_status(self):
        return self._DEBUG



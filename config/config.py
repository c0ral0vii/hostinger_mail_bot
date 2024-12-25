import os
from dotenv import load_dotenv


class Config:
    def __init__(self) -> None:
        load_dotenv()

        self._BOT_API = os.getenv('BOT_API')

        if not self._BOT_API:
            print('Не получен бота апи')

        # База данных
        self.DB_HOST = os.getenv('DB_HOST', '0.0.0.0')
        self.DB_NAME = os.getenv("DB_NAME", 'users')
        self.DB_USER = os.getenv("DB_USER", 'root')
        self.DB_PASS = os.getenv("DB_PASS", "root")
        self.DB_PORT = os.getenv("DB_PORT", 5432)

        self.DATABASE_URL = f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        print(self.DATABASE_URL)

        #
        self.BASE_HOST = 'mail.hostinger.com'

        #

        self._DEBUG = os.getenv("DEBUG", False)

        # Admins

        self._ADMIN_LIST = [345143657, 6408069387]

    def get_database_link(self):
        return rf'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    def get_bot_api(self):
        return self._BOT_API

    def get_debug_status(self):
        return self._DEBUG

    def get_base_host(self):
        return self.BASE_HOST

    def get_admin_list(self):
        return self._ADMIN_LIST


settings = Config()

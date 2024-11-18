import imaplib
from typing import NoReturn
from config.config import settings

class MailService:
    def __init__(self, password: int, email: str) -> None:
        self.password = password
        self.email = email

        self.server = settings.get_base_host()

    async def connect(self):
        """
        Подключение к почте

        :return:
        """

        ...
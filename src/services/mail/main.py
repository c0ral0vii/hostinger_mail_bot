import imaplib
import email
import re

from config.config import settings
from logger.logger import setup_logger


class MailService:
    def __init__(self,
                 password: str,
                 email_adress: str,
                 from_email: str,
                 logger=setup_logger(__name__)
                 ) -> None:

        self.imap_server = "imap.hostinger.com"

        self.logger = logger
        self.from_email = from_email
        self.password = password
        self.email_adress = email_adress

        self.server = settings.get_base_host()
        self._con = False


    async def connect(self):
        """
        Подключение к почте

        :return:
        """
        try:
            self.imap = imaplib.IMAP4_SSL(self.imap_server)
            self.logger.debug(f'{self.email_adress} is connected')
            self.imap.login(self.email_adress, self.password)
            self._con = True
        except Exception as e:
            self._con = False
            self.logger.error(f'{self.email_adress} is not connected: {e}')
            return {
                "status": '500',
                "error": e,
                "text": 'Не удалось подключиться',
            }

    async def disconnect(self):
        """
        Отключение от imap
        """
        if self._con:
            self.imap.close()
            return {
                'status': '200',
                'text': 'Отключено'
            }
        return {
            'status': '500',
            'text': "Подключения нет"
        }


    async def get_last_message(self):
        """
        Получение последнего сообщения
        """

        await self.connect()

        if not self._con:
            self.logger.info("Нет подключения к почтовому серверу")
            return {
                "status": "500",
                "text": "Нет подключения к почтовому серверу"
            }

        try:
            self.imap.select("INBOX")
            status, messages = self.imap.search(None, f'(TO "{self.from_email.strip()}")')
            self.logger.debug(f'(TO "{self.from_email.strip()}"): {messages})')

            if status != 'OK':
                self.logger.error("Не удалось получить список сообщений")
                return {
                    "status": "500",
                    "text": "Ошибка при поиске сообщений"
                }

            message_ids = messages[0].split()

            if not message_ids:
                self.logger.info("Сообщения отсутствуют")
                return {
                    "status": "204",
                    "text": "Сообщения отсутствуют"
                }

            for message_id in reversed(message_ids):
                status, msg_data = self.imap.fetch(message_id, '(RFC822)')

                if status != "OK":
                    self.logger.error(f"Ошибка при загрузке сообщения {message_id}")
                    continue

                msg = email.message_from_bytes(msg_data[0][1])
                self.logger.debug(f'Сообщение: {msg}')

                from_email = msg.get('From')
                subject = msg.get('Subject')

                code = ''

                # Проверяем части сообщения
                for part in msg.walk():
                    # Если сообщение имеет тип text/html
                    if part.get_content_type() == 'text/html':
                        html_content = part.get_payload(decode=True).decode('utf-8')

                        # Ищем 6-значный код внутри тега <h1>
                        code_match = re.search(r'<h1[^>]*>\s*(\d{6})\s*</h1>', html_content)
                        if code_match:
                            code = code_match.group(1)
                            self.logger.debug(f'Найденный код: {code}')
                            await self.disconnect()
                            return {
                                "status": "200",
                                "text": "Удалось получить последнее сообщение с кодом",
                                "from": from_email,
                                "subject": subject,
                                "code": code,
                            }

            await self.disconnect()
            return {
                "status": "200",
                "text": "Удалось получить последнее сообщение",
                "from": from_email,
                "subject": subject,
                "code": code,
            }

        except AttributeError as ae:
            self.logger.error(f'На почте -> {self.from_email} <- не найден код - {ae}')
            if self._con:
                await self.disconnect()

            return {
                "status": "500",
                "error": str(ae),
                "text": "Произошла неизвестная ошибка",
            }

        except Exception as e:
            self.logger.critical(f'Произошла ошибка {e}')
            if self._con:
                await self.disconnect()

            return {
                "status": "500",
                "error": str(e),
                "text": "Произошла неизвестная ошибка",
            }




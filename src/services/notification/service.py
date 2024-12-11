import asyncio
from datetime import date, datetime
from typing import Dict, Any

from aiogram import Bot, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from logger.logger import setup_logger
from src.services.database.orm.admins import get_all_admins
from src.services.database.orm.export import get_all_data
from src.services.database.orm.users import to_next_month


class Notification:
    def __init__(self,
                 bot: Bot,
                 logger=setup_logger(__name__),):
        self.logger = logger
        self._bot = bot
        self.skip = []
        self.messages: list[types.Message] = []

        self.time = [30, 60]

    async def start(self):
        try:
            if len(self.messages) >= 1:
                await self._delete_previous_message()

            await self._send_notification()

        except Exception as e:
            await asyncio.sleep(self.time[1])
            await self.start()

    async def _send_notification(self):
        all_users = await get_all_data()
        current_date = datetime.now().date()

        data = {}
        for user_id, user in all_users.items():
            if user.get("on_pause"):
                continue

            if isinstance(user.get("invoice_day"), date):
                days_left = (user.get("invoice_day")-current_date).days
                self.logger.debug(days_left)

                if days_left == 0:
                    await to_next_month(data={
                        "serial_number": user.get("serial_number")
                    })

                if 0 <= days_left <= 4:
                    data[user.get("serial_number", "Нет")] = days_left
            


        await self._send_messages(data=data)

    async def _send_messages(self, data: Dict[str, Any]):
        admins = await get_all_admins()

        for admin in admins:
            try:
                for serial_number, days_left in data.items():
                        message = await self._bot.send_message(chat_id=admin.user_id, text=f"⚠️По серийному номеру - {serial_number}\n⚠️Осталось дней - {days_left}", 
                                                    reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text="Перенести на следующий месяц", callback_data=f"next_month_{serial_number}")],
                        ])
                        )
                        self.messages.append(message)
            except Exception as e:
                self.logger.warning(f"Ошибка при отправке сообщения - {e}")
                continue

    
    async def _delete_previous_message(self):
        for message in self.messages:
            await message.delete()
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any

from aiogram import Bot

from logger.logger import setup_logger
from src.services.database.models import User
from src.services.database.orm.admins import get_all_admins
from src.services.database.orm.export import get_all_data


class Notification:
    def __init__(self,
                 bot: Bot,
                 logger=setup_logger(__name__),):
        self.logger = logger
        self._bot = bot
        self.time = [30, 60]

    async def start(self):
        try:
            await self._send_notification()

        except Exception as e:
            await asyncio.sleep(self.time[1])
            await self.start()

    async def _send_notification(self):
        all_users = await get_all_data()
        current_date = datetime.now()

        data = {}
        for user_id, user in all_users.items():
            if user.get("on_pause"):
                continue

            if isinstance(user.get("pay_day"), datetime):
                days_left = (user.get("pay_day")-current_date).days

                if 0 <= days_left <= 4:
                    data[user.get("serial_number", "Нет")] = days_left

        await self._send_messages(data=data)

    async def _send_messages(self, data: Dict[str, Any]):
        admins = await get_all_admins()

        for admin in admins:
            for serial_number, days_left in data.items():
                await self._bot.send_message(chat_id=admin.user_id, text=f"⚠️По серийному номеру - {serial_number}\n⚠️Осталось дней - {days_left}")
import asyncio
from datetime import datetime, timedelta

from aiogram import Bot

from src.services.database.models import User
from src.services.database.orm.export import get_all_data


class Notification:
    def __init__(self, bot: Bot):
        self._bot = bot
        self.message = "Скоро истечёт срок действия, произведите оплату"
        self.time = [30, 60, 120, 240, 360, 480, 1440, 86400]

    async def start(self):
        try:
            await self._send_notification()
            await asyncio.sleep(self.time[-1])

        except Exception as e:
            await asyncio.sleep(self.time[1])
            await self.start()

    async def _send_notification(self):
        all_users = await get_all_data()
        for user in all_users:
            if user["pre_pay_day"] - datetime.now() <= timedelta(days=5):
                await self._send_message(user["user_id"])

    async def _send_message(self, user_id: int):
        await self._bot.send_message(chat_id=user_id, text=self.message)
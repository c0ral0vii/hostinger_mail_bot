from aiogram.filters import Filter
from aiogram import Bot, types
from config.config import settings
from src.services.database.orm.admins import check_admin


class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in self.chat_types


class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        admins = await check_admin(data={
            "user_id": message.from_user.id,
        })

        if admins is True:
            return True

        return message.from_user.id in settings.get_admin_list()
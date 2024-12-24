from aiogram import Router, F, types
from logger.logger import setup_logger
from src.services.bot.filters.chat_type import ChatTypeFilter, IsAdmin
from src.services.database.orm.users import to_next_month as user_to_next_month

to_next_month_router = Router(name="to_next_month_router")
to_next_month_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

logger = setup_logger(__name__)


@to_next_month_router.callback_query(lambda query: 'next_month_' in query.data)
async def to_next_month(callback: types.CallbackQuery):
    callback_data = callback.data.split("_")[-1]

    await user_to_next_month({
        "serial_number": callback_data
    })

    await callback.message.answer(f"Продлено на месяц - {callback_data}")
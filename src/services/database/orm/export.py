from typing import Any, Dict

from sqlalchemy import select
from src.services.database.models import User, EMail
from src.services.database.database import async_session



async def get_all_data() -> Dict[str, Any]:
    async with async_session() as session:
        stmt = select(User)
        result = await session.execute(stmt)
        users = result.scalars().all()

        all_users = {}

        for user in users:
            u = {
                "serial_number": user.serial_number,
                "activated_date": user.activated_date,
                "pre_pay_day": user.need_pay_date,
                "pay_day": user.pay_date,
                "on_pause": user.stay_on_pause,
                "phone": f"+{user.user_number}",
                "tg_username": f"{user.telegram_user}",
                "username": user.username,
                "email": user.email,
                "password": user.password,
                "pay_list": user.pay_lists,
            }

            all_users[user.id] = u

        return all_users


async def get_all_data_emails() -> Dict[str, Any]:
    async with async_session() as session:
        stmt = select(EMail)
        result = await session.execute(stmt)
        emails = result.scalars().all()

        all_emails = {}

        for email in emails:
            e = {
                "email": email.email,
                "password": email.password,
            }

            all_emails[email.id] = e

        return all_emails
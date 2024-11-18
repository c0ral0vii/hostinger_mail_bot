from sqlalchemy import select

from typing import Dict, Any

from logger.logger import setup_logger
from src.services.database.database import async_session
from src.services.database.models import User


logger = setup_logger(__name__)


async def search_user(serial_number: str) -> Dict[str, Any]:
    async with async_session() as session:
        if not serial_number:
            return {
                "error": "Serial number is none",
                "text": "Вы ввели пустой серийный номер"
            }
        stmt = select(User).where(User.serial_number == serial_number)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            logger.critical(f'Не удаётся получить пользователя или такого серийного номера не существует {serial_number}')
            return {
                "error": "Not found",
                "text": "Вы не правильно ввели номер или его не существует"
            }

        return {
            "pay_date": user.pay_date,
            "email": user.email,
        }
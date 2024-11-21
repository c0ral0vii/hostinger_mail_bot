from sqlalchemy import select, or_

from typing import Dict, Any

from logger.logger import setup_logger
from src.services.database.database import async_session
from src.services.database.models import User


logger = setup_logger(__name__)


async def search_user(serial_number: str) -> Dict[str, Any]:
    """Поиск серийного номера"""
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


async def get_user_admin(find_str: str) -> Dict[str, Any]:
    """Поиск по базе админом"""
    async with async_session() as session:
        if not find_str:
            return {
                "error": "Serial number is none",
                "text": "Вы не ввели поисковой информации",
            }

        stmt = select(User).where(
            or_(
                User.serial_number == find_str,
                User.username == f'@{find_str}',
                User.email == find_str,
                User.user_number == int(find_str.replace('+', '').replace('-', '').replace(' ', '')),
            )
        )

        result = await session.execute(stmt)

        user = result.scalar_one_or_none()

        if not user:
            logger.critical(
                f'Не удаётся получить пользователя или такого серийного номера не существует {find_str}')
            return {
                "error": "Not found",
                "text": "Вы не правильно ввели номер или его не существует"
            }

        return {
            "user_id": f"ID: {user.id}",
            "serial_number": user.serial_number,
            "need_pay_date": user.need_pay_date,
            "stay_on_pause": user.stay_on_pause,
            "username": user.username,
            "pay_date": user.pay_date,
            "email": user.email,
            "password": user.password,
            "phone": user.user_number,
        }


async def get_email(username: str) -> Dict[str, Any]:
    async with async_session() as session:
        stmt = select(User).where(User.username == username)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            logger.critical(f'Не удалось получить пользователя @{username}')
            return {
                "error": "Not found",
                "text": "Не найдена привязанная к вам почта"
            }

        return {
            "status": "200",
            "to": username,
            "email": user.email,
            "password": user.password,
        }
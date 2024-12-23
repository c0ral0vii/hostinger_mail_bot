from sqlalchemy import select, or_

from typing import Dict, Any, NoReturn
from dateutil.relativedelta import relativedelta

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
            "pay_date": "-" if user.invoice_day is None else user.invoice_day.strftime("%d.%m.%Y"),
            "email": user.email,
            "password": user.password,
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
                User.telegram_user == f'{find_str}',
                User.email == find_str,
                User.user_number == find_str.replace('+', '').replace('-', '').replace(' ', ''),
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
            "user_id": f"ID: {user.id}" if {user.id} is not None else "ID: Не задано",
            "serial_number": user.serial_number,
            "need_pay_date": "-" if user.need_pay_date is None else user.need_pay_date.strftime("%d.%m.%Y"),
            "stay_on_pause": user.stay_on_pause,
            "username": user.username,
            "pay_date": "-" if user.invoice_day is None else user.invoice_day.strftime("%d.%m.%Y"),
            "email": user.email,
            "password": user.password,
            "phone": user.user_number,
            "comment": user.comment,
        }


async def get_email(cross_number: str) -> Dict[str, Any]:
    async with async_session() as session:
        stmt = select(User).where(User.serial_number == cross_number)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            logger.critical(f'Не удалось получить кросс номер -- {cross_number}')
            return {
                "error": "Not found",
                "text": "Не найдена привязанная к вам почта"
            }
        logger.debug(f"{user.email}: {user.password}")
        return {
            "status": "200",
            "email": user.email,
            "password": user.password,
        }
    

async def to_next_month(data: Dict[str, Any]) -> NoReturn:
    async with async_session() as session:
        stmt = select(User).where(User.serial_number == data.get("serial_number", None).upper())
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None:
            logger.warning(f"Перенос не удался, серийного номера не существует, {data.get("serial_number")}")
            return
        
        user.invoice_day = user.invoice_day + relativedelta(month=1)

        session.add(user)
        await session.commit()
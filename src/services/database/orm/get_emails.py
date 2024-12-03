from typing import Dict, Any

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from logger.logger import setup_logger
from src.services.database.database import async_session
from src.services.database.models import EMail

logger = setup_logger(__name__)\


async def get_emails():
    async with async_session() as session:
        stmt = select(EMail)
        result = await session.execute(stmt)
        emails = result.scalars().all()

        return emails


async def add_emails(data: Dict[str, Any]):
    async with async_session() as session:
        try:
            stmt = select(EMail).where(EMail.email == data['email'])
            result = await session.execute(stmt)
            email = result.scalar_one_or_none()

            if email:
                email.password = data['password']
                session.add(email)

            else:
                email = EMail(
                    email=data['email'],
                    password=data['password'],
                )
                session.add(email)

            await session.commit()
            logger.debug(f"Почта {data['email']} успешно сохранен")
        except IntegrityError as e:
            # Откат транзакции при ошибке целостности
            await session.rollback()
            logger.debug(f"Ошибка целостности данных: {e}")
        except Exception as e:
            await session.rollback()
            logger.debug(f"Ошибка при сохранении emails: {e}")
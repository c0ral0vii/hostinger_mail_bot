from sqlalchemy import select
from src.services.database.models import EverydayMessage
from src.services.database.database import async_session


async def create_everyday_message():
    async with async_session() as session:
        stmt = select(EverydayMessage).where(EverydayMessage.id == 1)
        result = await session.execute(stmt)
        message = result.scalar_one_or_none()
        if message:
            return message

        message = EverydayMessage(
            message = None,
        )

        session.add(message)
        await session.commit()

        return message


async def change_message(text: str):
    async with async_session() as session:
        stmt = select(EverydayMessage).where(EverydayMessage.id == 1)
        result = await session.execute(stmt)
        message = result.scalar_one_or_none()

        if message is None:
            return {
                "message": "Нет ежедневного сообщения"
            }

        message.message = text

        await session.commit()
        return {
            "data": message,
            "message": "Сообщение успешно изменилось"
        }
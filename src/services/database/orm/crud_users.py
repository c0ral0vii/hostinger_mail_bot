from sqlalchemy import select

from src.services.database.database import async_session
from src.services.database.models import User


async def change_login(serial_number: str, new_email: str):
    async with async_session() as session:
        stmt = select(User).where(User.serial_number == serial_number.upper())
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        user.email = new_email
        session.add(user)
        await session.commit()


async def change_nickname(serial_number: str, new_nickname: str):
    async with async_session() as session:
        stmt = select(User).where(User.serial_number == serial_number.upper())
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        user.username = new_nickname
        session.add(user)
        await session.commit()


async def change_comment(serial_number: str, new_comment: str):
    async with async_session() as session:
        stmt = select(User).where(User.serial_number == serial_number.upper())
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        user.comment = new_comment
        session.add(user)
        await session.commit()


async def change_password(serial_number: str, new_password: str):
    async with async_session() as session:
        stmt = select(User).where(User.serial_number == serial_number.upper())
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        user.password = new_password
        session.add(user)
        await session.commit()


async def change_pause(serial_number: str):
    async with async_session() as session:
        stmt = select(User).where(User.serial_number == serial_number.upper())
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if user.stay_on_pause is False:
            user.stay_on_pause = True
        elif user.stay_on_pause is True:
            user.stay_on_pause = False

        session.add(user)
        await session.commit()
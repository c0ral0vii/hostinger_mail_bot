from typing import Dict, Any

from sqlalchemy import select, delete

from src.services.database.database import async_session
from src.services.database.models import AdminUser


async def add_admin(data: Dict[str, Any], **kwargs) -> AdminUser.user_id:
    async with async_session() as session:
        try:
            admin = AdminUser(
                user_id=data["user_id"],
                username=data.get("username", 'Не задано'),
            )

            session.add(admin)
            await session.commit()

        except Exception as e:
            await session.rollback()


async def check_admin(data: Dict[str, Any], **kwargs):
    async with async_session() as session:
        stmt = select(AdminUser).where(AdminUser.user_id == data["user_id"]).limit(1)
        result = await session.execute(stmt)
        admin = result.scalar_one_or_none()

        if admin is None:
            return
        return True


async def delete_admin(data: Dict[str, Any], **kwargs) -> bool:
    async with async_session() as session:
        stmt = delete(AdminUser).where(AdminUser.user_id == data["user_id"])
        result = await session.execute(stmt)

        if result.rowcount > 0:
            await session.commit()
            return True
        else:
            return False


async def get_all_admins():
    async with async_session() as session:
        stmt = select(AdminUser)
        result = await session.execute(stmt)
        admins = result.scalars().all()

        return admins

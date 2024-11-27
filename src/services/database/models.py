from typing import List

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import Boolean, DateTime, Numeric, String, func, Integer, ForeignKey


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    user_number: Mapped[str] = mapped_column(String, nullable=False)
    telegram_user: Mapped[int] = mapped_column(String, nullable=False)

    need_pay_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    pay_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    activated_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    stay_on_pause: Mapped[bool] = mapped_column(Boolean, default=False)
    serial_number: Mapped[str] = mapped_column(String, nullable=False)

    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False) # password hashed

    pay_lists: Mapped[str] = mapped_column(String, nullable=True)

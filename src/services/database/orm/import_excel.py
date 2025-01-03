from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from src.services.database.models import User
from src.services.database.database import async_session

async def excel_import(data: dict) -> None:
    async with async_session() as session:
        try:
            stmt = select(User).where(User.serial_number == data['serial_number'])
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

            if user:
                # Обновление данных существующего пользователя
                user.telegram_user = data['telegram_username']
                user.activated_date = data.get('activated_date')
                user.need_pay_date = data.get('pay_day')
                user.invoice_day = data.get('invoice_day')
                user.stay_on_pause = data.get('on_pause')
                user.user_number = data.get('phone')
                user.username = data.get('username')
                user.email = data.get('email')
                user.password = data.get('password')
                user.pay_lists = str(data.get("pay_lists", 'Нет'))
                user.comment = str(data.get("comment"))
            else:
                # Создание нового пользователя
                user = User(
                    serial_number=data.get('serial_number').upper(),
                    activated_date=data.get('activated_date'),
                    need_pay_date=data.get('pay_day'),
                    invoice_day=data.get('invoice_day'),
                    stay_on_pause=data.get('on_pause'),
                    user_number=data.get('phone'),
                    telegram_user=data.get('telegram_username'),
                    username=data.get('username', 'Нет'),
                    email=data.get('email', 'Нет'),
                    password=data.get('password', 'Нет'),
                    pay_lists=str(data.get("pay_lists", 'Нет')),
                    comment = str(data.get("comment"))
                )
                session.add(user)

            # Фиксация изменений в базе данных
            await session.commit()
            print(f"Пользователь {data['telegram_username']} успешно сохранен")
        except IntegrityError as e:
            # Откат транзакции при ошибке целостности
            await session.rollback()
            print(f"Ошибка целостности данных: {e}")
        except Exception as e:
            # Откат транзакции при любой другой ошибке
            await session.rollback()
            print(f"Ошибка при сохранении пользователя: {e}")

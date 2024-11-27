from aiogram import Router, F, types
from src.services.mail.main import MailService
from src.services.database.orm.users import get_email
from logger.logger import setup_logger

get_code_router = Router(name="get_code")

logger = setup_logger(__name__)


@get_code_router.message(F.text == 'Получить код с почты')
async def get_code_from_mail(message: types.Message):
    username = f'@{message.from_user.username}'

    message = await message.answer("Получаем код...")
    mail_data = await get_email(username=username)

    mail_service = await MailService(email_adress="Extra@zov.icu", password="Vitalik1!!!").get_last_message()

    if mail_service.get('status') == "200":
        await message.delete()
        logger.info(f"Пользователь запросил код с почты {username}")
        await message.answer(f"-> {mail_service.get('code')} <-")
    else:
        await message.answer(f"""Не удалось получить код с почты""")
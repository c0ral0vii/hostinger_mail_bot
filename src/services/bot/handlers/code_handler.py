from aiogram import Router, F, types

from src.services.database.orm.get_emails import get_emails
from src.services.mail.main import MailService
from src.services.database.orm.users import get_email
from logger.logger import setup_logger

get_code_router = Router(name="get_code")

logger = setup_logger(__name__)


@get_code_router.callback_query(lambda query: 'get_code_' in query.data)
async def get_code_from_mail(callback: types.CallbackQuery):
    cross_number = callback.data.split("_")[-1]

    message = await callback.message.answer("Получаем код...")
    mail_data = await get_email(cross_number=cross_number.upper())
    emails = await get_emails()

    for email in emails:
        if "gmail.com" in email.email:
            continue
        if email.email.split("@")[-1].strip() != mail_data["email"].split("@")[-1].strip():
            continue

        mail_service = await MailService(from_email=mail_data["email"], email_adress=email.email, password=email.password).get_last_message()
        if mail_service.get('status') == "200":
            logger.info(f"Запрошен серийный номер -- {cross_number}")
            await message.delete()
            await callback.message.answer(f"{mail_service.get('code')}")
            return
        if mail_service.get('status') == "500":
            continue
        if mail_service.get('status') == "204":
            continue
    await message.delete()
    await callback.message.answer(f"""Не удалось получить код с почты""")
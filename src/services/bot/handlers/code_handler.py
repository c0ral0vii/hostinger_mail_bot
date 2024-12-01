from aiogram import Router, F, types
from src.services.mail.main import MailService
from src.services.database.orm.users import get_email
from logger.logger import setup_logger

get_code_router = Router(name="get_code")

logger = setup_logger(__name__)


@get_code_router.callback_query(lambda query: 'get_code_' in query.data)
async def get_code_from_mail(callback: types.CallbackQuery):
    cross_number = callback.data.split("_")[-1]

    message = await callback.message.answer("Получаем код...")
    mail_data = await get_email(cross_number=cross_number)

    mail_service = await MailService(from_email=mail_data["email"], email_adress="Extra@zov.icu", password="Vitalik1!!!").get_last_message()

    if mail_service.get('status') == "200":
        # await callback.message.delete()
        logger.info(f"Запрошен серийный номер -- {cross_number}")
        await callback.message.answer(f"-> {mail_service.get('code')} <-")
    else:
        await callback.message.answer(f"""Не удалось получить код с почты""")
import os
import pandas as pd
from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.exc import IntegrityError

from logger.logger import setup_logger
from src.services.bot.filters.chat_type import ChatTypeFilter, IsAdmin
from src.services.bot.fsm.user_states import FileState
from src.services.database.orm.get_emails import add_emails

add_emails_router = Router(name='add_emails_router')
add_emails_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())

logger = setup_logger(__name__)

@add_emails_router.message(F.text == "Изменить почты")
async def change_emails(message: types.Message, state: FSMContext):
    logger.info(f'Импорт @{message.from_user.username}')
    await message.answer('Отправьте файл .xlsx')
    await state.set_state(FileState.email_file)

@add_emails_router.message(F.document, StateFilter(FileState.email_file))
async def state_change_email(message: types.Message, state: FSMContext):
    document_id = message.document.file_id
    file = await message.bot.get_file(document_id)

    # Создаем временный каталог, если он не существует
    temp_dir = '/temp'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    file_path = os.path.join(temp_dir, 'import_emails.xlsx')
    await message.bot.download_file(file.file_path, file_path)

    try:
        df = pd.read_excel(file_path, header=None, engine='openpyxl')

        # Проверка на наличие необходимых столбцов
        if df.shape[1] < 2:
            await message.answer("Файл не содержит необходимых столбцов (email, password)")
            return

        for index, row in df.iterrows():
            if row[0] == 'email':
                continue
            email = row[0]
            password = row[1]

            data = {'email': email, 'password': password}

            try:
                await add_emails(data=data)
            except IntegrityError as e:
                await message.answer(f"Ошибка целостности данных для email {email}: {e}")
            except Exception as e:
                await message.answer(f"Ошибка при обработке email {email}: {e}")

        await message.answer("База данных обновлена успешно!")
    except Exception as e:
        await message.answer(f"Ошибка при обработке файла: {e}")
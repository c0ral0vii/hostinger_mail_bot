import asyncio
from datetime import datetime

from logger.logger import setup_logger
from src.services.database.orm.export import get_all_data
from src.services.export_excel.services import create_export_file_users


class DatabaseSaverService:
    def __init__(self,
                 logger=setup_logger(__name__),):
        self.loger = logger
        self.timeout = [30]

    async def start_save(self):
        try:
            await self._create_file()
        except Exception as e:
            self.loger.warning(e)
            await asyncio.sleep(self.timeout[0])

    async def _create_file(self):
        all_data = await get_all_data()
        backup_name = datetime.strftime(datetime.now(), '%Y-%m-%d_%H:%M:%S')+'_db_backup'
        await create_export_file_users(data=all_data, filename=backup_name, to_temp=True)
from src.services.database.models import User


class Notification:
    def __init__(self, check_list: list[User]):
        self.check_list = []
        self.time = [30, 60, 120, 240, 360, 480, 1440]

    async def check(self):
        ...

    async def send_notification(self):
        ...

    async def delete(self):
        ...
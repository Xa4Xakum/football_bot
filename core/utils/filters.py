from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message

from core.utils.operations import MiddleLevel
from config import Config


class ChatType(BaseFilter):
    def __init__(self, chat_type: Union[str, list]):
        self.chat_type = chat_type

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.chat_type, str):
            return message.chat.type == self.chat_type
        else:
            return message.chat.type in self.chat_type


class Admin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        ml = MiddleLevel()
        return ml.is_admin(message.from_user.id)


class GrandAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        conf = Config()
        return message.from_user.id == conf.get_grand_admin_id()

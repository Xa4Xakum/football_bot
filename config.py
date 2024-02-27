import os
from dotenv import load_dotenv
from enum import Enum


class Modes(Enum):
    test: str = 'test'
    production: str = 'prod'


class Config():

    def __init__(self, mode=Modes.production.value) -> None:
        self.mode = mode
        load_dotenv()


    def get_bot_token(self) -> str:
        '''
        Возвращает токен бота
        '''
        if self.mode == Modes.test.value: return os.getenv('TEST_TOKEN')
        elif self.mode == Modes.production.value: return os.getenv('TOKEN')


    def get_db_connection(self) -> str:
        '''
        Возвращает подключение к бд
        '''
        return 'sqlite:///core/xakum.db'


    def get_grand_admin_id(self) -> int:
        '''
        Возвращает айди главного админа(владельца)
        '''
        return int(os.getenv('GRAND_ADMIN'))


    def get_report_chat(self) -> int:
        '''
        Возвращает чат для репортов
        '''
        return int(os.getenv('REPORT_CHAT'))

from core.utils.database import DataBase

from config import Config


class MiddleLevel():


    def is_admin(self, user_id: int) -> bool:
        '''Проверка на админа'''

        db = DataBase()
        conf = Config()
        admin = db.get_admin(user_id)

        if admin: is_admin = True
        else: is_admin = False
        if user_id == conf.get_grand_admin_id(): is_admin = True

        return is_admin

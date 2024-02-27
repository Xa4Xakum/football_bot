from datetime import datetime
from typing import Union, List

from sqlalchemy import create_engine, String, Column, DateTime, BigInteger, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func

from config import Config


class DataBase:
    '''
    Класс для работы с базой данных
    '''
    __instance = None
    conf = Config()
    engine = create_engine(conf.get_db_connection(), echo=False, isolation_level="AUTOCOMMIT", pool_pre_ping=True)
    Session = sessionmaker(autoflush=False, bind=engine)
    Base = declarative_base()



    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(DataBase, cls).__new__(cls)
        return cls.__instance


    class Users(Base):
        __tablename__ = "users"

        user_id = Column(BigInteger(), primary_key=True)
        last_mail_seen = Column(DateTime())
        wantmail = Column(Boolean())


    class Promocodes(Base):
        __tablename__ = "promocodes"

        promo = Column(String(), primary_key=True)
        ref_link = Column(String())
        cite = Column(String())


    class Translations(Base):
        __tablename__ = 'translations'


        translation_id = Column(BigInteger(), primary_key=True)
        link = Column(String())
        description = Column(String())


    class Admins(Base):
        __tablename__ = 'admins'

        admin_id = Column(BigInteger(), primary_key=True)
        username = Column(String())
        role = Column(String())


    Base.metadata.create_all(engine, checkfirst=True)  # создание таблиц


    def add_admin(self, admin_id: int, username: str, role='base') -> None:
        '''
        Добавляет админа в бд

        :param admin_id: айди админа в тг
        :param role: роль админа(в будущем)
        '''

        with self.Session() as s:
            admin = self.Admins(
                admin_id=admin_id,
                username=username,
                role=role
            )
            s.add(admin)
            s.commit()


    def del_admin(self, admin_id: int) -> None:
        '''
        Удаляет админа из бд

        :param admin_id: id админа
        '''

        with self.Session() as s:
            s.query(self.Admins).filter(
                self.Admins.admin_id == admin_id
            ).delete()
            s.commit()


    def get_admin(self, admin_id: int) -> Union[Admins, None]:
        '''
        Возвращает запись об админе
        '''

        with self.Session() as s:
            return s.query(self.Admins).filter(
                self.Admins.admin_id == admin_id
            ).first()


    def get_all_admins(self) -> List[Admins]:
        '''
        Возвращает записи о всех админах
        '''

        with self.Session() as s:
            return s.query(self.Admins).all()


    def get_all_translations(self) -> List[Translations]:
        '''
        Возвращает лист трансляций
        '''

        with self.Session() as s:
            return s.query(self.Translations).all()


    def add_translation(self, link: str, description: str) -> None:
        '''
        Добавляет ссылку на трансляцию

        :param link: Ссылка на трансляцию
        :param description: Описание трансляции
        '''

        with self.Session() as s:
            translation = self.Translations(
                translation_id=self.get_max_translation_id() + 1,
                link=link,
                description=description
            )
            s.add(translation)
            s.commit()


    def delete_translation(self, translation_id: int) -> None:
        '''
        Удаляет трансляцию по айдишнику

        :param translation_id: Айди трансляции
        '''

        with self.Session() as s:
            s.query(self.Translations).filter(
                self.Translations.translation_id == translation_id
            ).delete()
            s.commit()


    def get_max_translation_id(self) -> int:
        with self.Session() as session:
            result = session.query(func.max(self.Translations.translation_id)).scalar()
            if result is not None:
                return result
            return 0


    def delete_user(self, user_id) -> None:
        '''
        Удаляет пользователя из бд

        :param user_id: Айди пользователя в тг
        '''

        with self.Session() as s:
            s.query(self.Users).filter(
                self.Users.user_id == user_id
            ).delete()
            s.commit()


    def get_all_users(self) -> List[Users]:
        '''
        Возвращает список всех пользователей
        '''

        with self.Session() as s:
            return s.query(self.Users).all()


    def add_user(self, user_id: int, last_mail_seen: datetime, wantmail=True) -> None:
        '''
        Добавляет пользователя в бд

        :param user_id: ID Пользователя в тг
        :param last_mail_seen: Последний показ рассылки
        :param want_mail: Хочет ли пользователь видеть рассылку
        '''

        with self.Session() as s:
            user = self.Users(
                user_id=user_id,
                last_mail_seen=last_mail_seen,
                wantmail=wantmail
            )
            s.add(user)
            s.commit()


    def get_user(self, user_id: int) -> Union[Users, None]:
        '''
        Возвращает запись о пользователе в бд

        :param user_id: Айди пользователя в тг
        '''

        with self.Session() as s:
            return s.query(self.Users).filter(
                self.Users.user_id == int(user_id)
            ).first()


    def add_promo(self, promo: str, ref_link: str, cite: str) -> None:
        '''
        Добавляет промокод в бд

        :param promo: Сам промокод
        :param ref_link: Реферальная ссылка на сайт, где работает промик
        :param cite: Название сайта/сервиса, где работает промик
        '''

        with self.Session() as s:
            promo = self.Promocodes(
                promo=promo,
                ref_link=ref_link,
                cite=cite
            )
            s.add(promo)
            s.commit()


    def get_promo(self, promo: str) -> Union[Promocodes, None]:
        '''
        Возвращает промокод из бд

        :param promo: Сам промокод
        '''

        with self.Session() as s:
            return s.query(self.Promocodes).filter(
                self.Promocodes.promo == promo
            ).first()


    def delete_promo(self, promo: str) -> None:
        '''
        Удаляет промик

        :param promo: Сам промокод
        '''

        with self.Session() as s:
            s.query(self.Promocodes).filter(
                self.Promocodes.promo == promo
            ).delete()
            s.commit()


    def get_all_promos(self) -> List[Promocodes]:
        '''
        Возвращает список всех промокодов
        '''

        with self.Session() as s:
            return s.query(self.Promocodes).all()

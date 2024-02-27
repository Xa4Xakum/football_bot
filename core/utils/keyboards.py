
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


class UserButtons():
    '''Кнопки пользователей'''

    translations = KeyboardButton(text='Трансляции')
    promocodes = KeyboardButton(text='К промокодам')
    help_btn = KeyboardButton(text='Помощь')
    report = KeyboardButton(text='Пожаловаться')

    promocode = KeyboardButton(text='Промокод')
    translation = KeyboardButton(text='Трансляция')
    bug = KeyboardButton(text='Баг')
    feedback = KeyboardButton(text='Обратная связь')

    to_menu = KeyboardButton(text='В меню')


class AdminButtons():
    '''Кнопки админов'''

    add_promo = KeyboardButton(text='Добавить промокод')
    delete_promo = KeyboardButton(text='Удалить промокод')
    admin_menu_btn = KeyboardButton(text='В меню админа')
    add_translation = KeyboardButton(text='Добавить трансляцию')
    delete_translation = KeyboardButton(text='Удалить трансляцию')
    all_good = KeyboardButton(text='Все верно')
    reenter = KeyboardButton(text='Ввести заново')
    confirm = KeyboardButton(text='Подтвердить')
    cancel = KeyboardButton(text='Отменить')
    list_admins = KeyboardButton(text='Список админов')
    mail_btn = KeyboardButton(text='Рассылка')


class Buttons(UserButtons, AdminButtons):
    '''Все кнопки бота'''


class UserKeyboards(Buttons):
    '''Клавиатуры пользователей'''

    def user_menu(self, with_admin_menu=False) -> ReplyKeyboardMarkup:
        '''
        Возваращает клаву пользователей

        :param with_admin_menu: Добавить кнопку перехода в меню админа
        '''

        builder = ReplyKeyboardBuilder()
        if with_admin_menu: builder.add(self.admin_menu_btn)

        builder.add(
            self.translations,
            self.promocodes,
            self.report
        )

        return builder.as_markup(resize_keyboard=True)


    def to_menu_markup(self) -> ReplyKeyboardMarkup:
        '''
        Возвращает клавиатуру перехода в меню пользователя
        '''

        builder = ReplyKeyboardBuilder()

        builder.add(
            self.to_menu
        )

        return builder.as_markup(resize_keyboard=True)


    def report_markup(self) -> ReplyKeyboardMarkup:
        '''
        Возвращает клаву отправки репорта
        '''

        builder = ReplyKeyboardBuilder()
        builder.add(
            self.translation,
            self.promocode,
            self.bug,
            self.feedback
        )
        builder.adjust(2)

        return builder.as_markup(resize_keyboard=True)


class AdminKeyboards(Buttons):
    '''Клавиатуры админов'''


    def admin_menu(self, grand_admin=False) -> ReplyKeyboardMarkup:
        '''Клавиатура меню админа'''

        builder = ReplyKeyboardBuilder()
        if grand_admin:
            builder.add(
                self.list_admins,
                self.mail_btn
            )

        builder.add(
            self.add_promo,
            self.delete_promo,
            self.add_translation,
            self.delete_translation
        )
        builder.adjust(2)

        return builder.as_markup(resize_keyboard=True)


    def check_correct(self) -> ReplyKeyboardMarkup:
        '''Клавиатура проверки правильности ввода'''

        builder = ReplyKeyboardBuilder()
        builder.add(
            self.all_good,
            self.reenter
        )

        return builder.as_markup(resize_keyboard=True)


    def confirm_markup(self) -> ReplyKeyboardMarkup:
        '''Клавиатура подтверджения или отклонения'''

        builder = ReplyKeyboardBuilder()
        builder.add(
            self.confirm,
            self.cancel
        )

        return builder.as_markup(resize_keyboard=True)


class Keyboards(UserKeyboards, AdminKeyboards):
    '''Все клавиатуры бота'''

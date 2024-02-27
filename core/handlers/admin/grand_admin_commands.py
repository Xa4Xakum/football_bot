from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from core.utils.filters import GrandAdmin
from core.utils.keyboards import Keyboards
from core.utils.database import DataBase


r = Router()
r.message.filter(
    GrandAdmin()
)


@r.message(Command('id'))
async def get_id(msg: Message):
    text = (
        f'chat_id: <code>{msg.chat.id}</code>\n'
        f'msg_id: <code>{msg.message_id}</code>\n'
        f'from_user_id: <code>{msg.from_user.id}</code>\n'
    )

    if msg.reply_to_message:
        text += (
            f'reply_to_msg_from_user_id: <code>{msg.reply_to_message.from_user.id}\n</code>'
            f'reply_to_msg_from_username: <code>{msg.reply_to_message.from_user.username}\n</code>'
        )

    await msg.answer(text=text, parse_mode='html')


@r.message(Command('addadmin'))
async def add_admin(msg: Message):

    db = DataBase()
    if msg.reply_to_message:
        admin_id = msg.reply_to_message.from_user.id
        username = msg.reply_to_message.from_user.username
    else:
        params = msg.text.split()
        admin_id = int(params[1])
        username = params[2]

    admin = db.get_admin(admin_id)
    if admin:
        await msg.answer('Такой админ уже есть')
        return

    db.add_admin(admin_id, username)
    await msg.answer('Админ успешно добавлен!')


@r.message(Command('deladmin'))
async def del_admin(msg: Message):

    db = DataBase()

    if msg.reply_to_message:
        admin_id = msg.reply_to_message.from_user.id
    else:
        params = msg.text.split()
        admin_id = int(params[1])

    admin = db.get_admin(admin_id)
    if admin is None:
        await msg.answer('Такого админа нет в моей бд..')
        return

    db.del_admin(admin_id)
    await msg.answer('Админ успешно удален!')


@r.message(F.text == Keyboards.list_admins.text)
async def list_admins(msg: Message):
    db = DataBase()

    admins = db.get_all_admins()
    text = 'Вот список всех админов:\n\n'
    for admin in admins:
        text += (
            f'id: <code>{admin.admin_id}</code>\n'
            f'username: @<code>{admin.username}</code>\n'
            f'role: <code>{admin.role}</code>\n\n'
        )

    await msg.answer(text, parse_mode='html')

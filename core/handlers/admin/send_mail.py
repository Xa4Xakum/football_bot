import asyncio

from datetime import datetime

import math

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from loguru import logger

from core.utils.filters import ChatType, Admin
from core.utils.keyboards import Keyboards
from core.utils.states import Mail
from core.utils.database import DataBase


r = Router()
r.message.filter(
    ChatType('private'),
    Admin()
)


@r.message(F.text == Keyboards.mail_btn.text)
async def start_mail(msg: Message, state: FSMContext):
    await msg.answer('Отправьте сообщение для рассылки(с одним вложением)')
    await state.set_state(Mail.get_content)


@r.message(StateFilter(Mail.get_content))
async def get_mail_content(msg: Message, state: FSMContext):
    db = DataBase()
    users = db.get_all_users()
    start_time = datetime.now()
    kb = Keyboards()

    text = (
        f'Начинаю рассылку\n\n'
        f'Число пользователей: {len(users)}\n'
        f'Примерное время рассылки: {math.ceil(len(users)*1.1)} секунд'
    )

    await msg.answer(text)

    sended = 0
    errored = 0

    for i in users:
        try:
            await msg.copy_to(i.user_id)
            sended += 1

        except Exception as e:
            await logger.warning(f'Не удалось отправить сообщение пользователю {i.user_id} по причине {e}, удаляю его из бд..')
            db.delete_user(i.user_id)
            errored += 1

        await asyncio.sleep(1)

    end_time = datetime.now()
    taked_tame = (end_time - start_time).seconds

    hours = taked_tame // 3600
    minutes = (taked_tame % 3600) // 60
    secounds = (taked_tame % 60) // 1

    text = (
        f'Рассылка отправлена {len(users)} пользователям\n'
        f'Удачно: {sended}\n'
        f'неудачно: {errored}\n'
        f'Общее время: {hours}:{minutes}:{secounds}\n'
    )

    await msg.answer(text, reply_markup=kb.to_menu_markup())
    await state.set_data({})
    await state.set_state(None)

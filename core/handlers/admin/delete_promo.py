from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from core.utils.filters import ChatType, Admin
from core.utils.keyboards import Keyboards
from core.utils.states import DeletePromo
from core.utils.database import DataBase

r = Router()
r.message.filter(
    ChatType('private'),
    Admin()
)


@r.message(F.text == Keyboards.delete_promo.text)
async def start_delete_promo(msg: Message, state: FSMContext):
    await msg.answer('Введите промокод, который хотите удалить')
    await state.set_state(DeletePromo.get_promo)


@r.message(F.text, StateFilter(DeletePromo.get_promo))
async def get_promo(msg: Message, state: FSMContext):
    db = DataBase()
    promo = db.get_promo(msg.text)
    kb = Keyboards()

    if promo is None:
        await msg.answer('Я не нашел такой промокод в своей базе данных')
        await state.set_state(None)

    await state.update_data(promo=msg.text)
    text = (
        f'Я нашел такой промокод:\n'
        f'{promo.cite} {promo.promo} {promo.ref_link}\n\n'
        f'Вы действительно хотите его удалить?'
    )
    await msg.answer(text, reply_markup=kb.confirm_markup())
    await state.set_state(DeletePromo.confirm)


@r.message(F.text == Keyboards.confirm.text, StateFilter(DeletePromo.confirm))
async def delete_promo(msg: Message, state: FSMContext):
    db = DataBase()
    data = await state.get_data()
    kb = Keyboards()

    db.delete_promo(data['promo'])
    await msg.answer('Промокод успешно удален!', reply_markup=kb.to_menu_markup())

    await state.set_data({})
    await state.set_state(None)


@r.message(F.text == Keyboards.cancel.text, StateFilter(DeletePromo.confirm))
async def cancel_delete_promo(msg: Message, state: FSMContext):
    await msg.answer('Промокод не удален')

    await state.set_data({})
    await state.set_state(None)

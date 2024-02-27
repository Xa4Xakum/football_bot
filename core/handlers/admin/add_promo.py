from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from core.utils.filters import ChatType, Admin
from core.utils.keyboards import Keyboards
from core.utils.states import AddPromo
from core.utils.database import DataBase

r = Router()
r.message.filter(
    ChatType('private'),
    Admin()
)


@r.message(F.text == Keyboards.reenter.text, StateFilter(AddPromo.check_correct))
@r.message(F.text == Keyboards.add_promo.text)
async def start_add_promo(msg: Message, state: FSMContext):

    await msg.answer(
        text='Отправьте промокод\n'
    )
    await state.set_state(AddPromo.get_promo_text)


@r.message(F.text, StateFilter(AddPromo.get_promo_text))
async def get_promo_text(msg: Message, state: FSMContext):
    await state.update_data(promo=msg.text)
    await msg.answer('Отправьте сайт(можно реферальную ссылку), на котором этот промокод можно использовать')
    await state.set_state(AddPromo.get_ref_link)


@r.message(F.text, StateFilter(AddPromo.get_ref_link))
async def get_ref_link(msg: Message, state: FSMContext):
    await state.update_data(ref_link=msg.text)
    await msg.answer('Отправьте название сайта/сервиса(1win, фонбет, лига ставок)')
    await state.set_state(AddPromo.get_cite)


@r.message(F.text, StateFilter(AddPromo.get_cite))
async def get_cite(msg: Message, state: FSMContext):
    await state.update_data(cite=msg.text)
    kb = Keyboards()
    data = await state.get_data()
    text = (
        f'Проверьте правильность данных:\n\n'
        f'Сайт: {data["cite"]}\n'
        f'Промокод: {data["promo"]}\n'
        f'Ссылка: {data["ref_link"]}\n'
    )
    await msg.answer(text, reply_markup=kb.check_correct())
    await state.set_state(AddPromo.check_correct)


@r.message(F.text == Keyboards.all_good.text, StateFilter(AddPromo.check_correct))
async def add_promo_end(msg: Message, state: FSMContext):

    db = DataBase()
    data = await state.get_data()
    kb = Keyboards()

    promo = db.get_promo(data['promo'])

    if promo:
        await msg.answer(
            f'Такой промокод уже есть\n'
            f'Его данные:\n\n'
            f'{promo.cite} {promo.promo} {promo.ref_link}'
        )
        await state.set_state(None)
        await state.set_data({})
        return

    db.add_promo(
        promo=data['promo'],
        ref_link=data['ref_link'],
        cite=data['cite']
    )

    await msg.answer('Промокод успешно добавлен!', reply_markup=kb.to_menu_markup())
    await state.set_data({})
    await state.set_state(None)

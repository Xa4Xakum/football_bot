from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from core.utils.filters import ChatType, Admin
from core.utils.keyboards import Keyboards
from core.utils.states import AddTranslation
from core.utils.database import DataBase

r = Router()
r.message.filter(
    ChatType('private'),
    Admin()
)


@r.message(F.text == Keyboards.reenter.text, StateFilter(AddTranslation.check_correct))
@r.message(F.text == Keyboards.add_translation.text)
async def start_add_translation(msg: Message, state: FSMContext):
    await msg.answer('Отправьте ссылку на чат, где будет ссылка на трансляцию')
    await state.set_state(AddTranslation.get_link)


@r.message(F.text, StateFilter(AddTranslation.get_link))
async def get_link(msg: Message, state: FSMContext):
    await state.update_data(link=msg.text)
    await msg.answer('Отправьте описание трансляции(к примеру, трансляция по футболу)')
    await state.set_state(AddTranslation.get_description)


@r.message(F.text, StateFilter(AddTranslation.get_description))
async def get_description(msg: Message, state: FSMContext):
    kb = Keyboards()
    await state.update_data(description=msg.text)
    data = await state.get_data()
    text = (
        f'Проверьте правильность:\n\n'
        f'{data["link"]}\n\n'
        f'{data["description"]}'
    )

    await msg.answer(text, reply_markup=kb.check_correct())
    await state.set_state(AddTranslation.check_correct)


@r.message(F.text == Keyboards.all_good.text, StateFilter(AddTranslation.check_correct))
async def add_translation_end(msg: Message, state: FSMContext):
    data = await state.get_data()
    db = DataBase()
    kb = Keyboards()

    db.add_translation(
        link=data['link'],
        description=data['description']
    )

    await msg.answer('Трансляция успешно добавлена!', reply_markup=kb.to_menu_markup())
    await state.set_data({})
    await state.set_state(None)

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from core.utils.filters import ChatType, Admin
from core.utils.keyboards import Keyboards
from core.utils.states import DeleteTranslation
from core.utils.database import DataBase

r = Router()
r.message.filter(
    ChatType('private'),
    Admin()
)


@r.message(F.text == Keyboards.delete_translation.text)
async def start_delete_translation(msg: Message, state: FSMContext):
    db = DataBase()
    translations = db.get_all_translations()
    builder = InlineKeyboardBuilder()

    text = 'Список имеющихся трансляций:\n\n'

    for i in translations:
        text += f'{i.translation_id}. {i.link}\n{i.description}\n\n'
        builder.add(InlineKeyboardButton(text=str(i.translation_id), callback_data=str(i.translation_id)))

    builder.adjust(3)
    text += 'Чтобы удалить трансляцию, выберите кнопку'

    await msg.answer(text=text, reply_markup=builder.as_markup())
    await state.set_state(DeleteTranslation.get_translation_id)


@r.callback_query(StateFilter(DeleteTranslation.get_translation_id))
async def delete_translation(call: CallbackQuery, state: FSMContext):

    translation_id = int(call.data)
    db = DataBase()
    db.delete_translation(translation_id=translation_id)
    kb = Keyboards()

    await call.message.answer('Трансляция успешно удалена!', reply_markup=kb.to_menu_markup())
    await state.set_state(None)
    await state.set_data({})

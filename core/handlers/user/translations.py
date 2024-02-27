from aiogram import Router, F
from aiogram.types import Message
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.utils.filters import ChatType
from core.utils.database import DataBase
from core.utils.keyboards import Keyboards


r = Router()
r.message.filter(
    ChatType('private')
)


@r.message(F.text == Keyboards.translations.text)
async def translations(msg: Message):

    db = DataBase()
    trans = db.get_all_translations()
    builder = InlineKeyboardBuilder()

    text = 'Вот список актуальных трансляций:\n\n'
    for tran in trans:
        text += (
            f'{tran.translation_id}. {tran.link} - {tran.description}\n'
        )
        builder.add(InlineKeyboardButton(text=str(tran.translation_id), url=tran.link))

    builder.adjust(3)

    await msg.answer(text=text, reply_markup=builder.as_markup())

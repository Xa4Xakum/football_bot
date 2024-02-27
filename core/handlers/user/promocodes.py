from aiogram import Router, F
from aiogram.types import Message

from core.utils.filters import ChatType
from core.utils.database import DataBase
from core.utils.keyboards import Keyboards


r = Router()
r.message.filter(
    ChatType('private')
)


@r.message(F.text == Keyboards.promocodes.text)
async def promocodes(msg: Message):

    db = DataBase()
    proms = db.get_all_promos()
    kb = Keyboards()

    text = (
        'Вот список всех доступных промокодов (запись в формате сервис, '
        'где испольуется промокод - промокод - ссылка на сервис):\n\n'
    )

    for promo in proms:
        text += f'{promo.cite} - <code>{promo.promo}</code> - {promo.ref_link}\n'

    text += (
        '\nЕсли какой-то из промокодов оказался нерабочим, просто скопируйте его, '
        'в меню нажмите "пожаловаться", выберите "промокод" и далее следуйте инструкциям'
    )
    await msg.answer(text, parse_mode='html', reply_markup=kb.to_menu_markup())

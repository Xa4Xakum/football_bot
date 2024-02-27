from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from core.utils.filters import ChatType
from core.utils.database import DataBase
from core.utils.keyboards import Keyboards
from core.utils.operations import MiddleLevel


r = Router()
r.message.filter(
    ChatType('private')
)


@r.message(F.text == Keyboards.to_menu.text)
@r.message(F.text, Command('start'))
async def start(msg: Message, state: FSMContext):

    db = DataBase()
    kb = Keyboards()
    ml = MiddleLevel()

    await state.set_state(None)
    await state.set_data({})

    user = db.get_user(msg.from_user.id)
    if user is None:
        db.add_user(
            user_id=msg.from_user.id,
            last_mail_seen=datetime.now()
        )

    text = (
        'Добро пожаловать в меню!\n'
        'У меня всегда есть свежая ссылка на трансляции, '
        'а так же набор промокодов, для любителей ставок! '
    )

    await msg.answer(
        text=text,
        reply_markup=kb.user_menu(with_admin_menu=ml.is_admin(msg.from_user.id))
    )

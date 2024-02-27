from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from core.utils.filters import ChatType, Admin
from core.utils.keyboards import Keyboards

from config import Config

r = Router()
r.message.filter(
    ChatType('private'),
    Admin()
)


@r.message(F.text == Keyboards.admin_menu_btn.text)
async def start(msg: Message, state: FSMContext):

    keyboards = Keyboards()
    await state.set_state(None)
    conf = Config()

    await msg.answer(
        text='Добро пожаловать в меню админа!\n',
        reply_markup=keyboards.admin_menu(msg.from_user.id == conf.get_grand_admin_id())
    )

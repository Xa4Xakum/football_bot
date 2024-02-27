from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from core.utils.filters import ChatType
from core.utils.keyboards import Keyboards
from core.utils.states import SendReport

from config import Config
from helper import bot

r = Router()
r.message.filter(
    ChatType('private')
)


@r.message(F.text == Keyboards.report.text)
async def start_send_report(msg: Message, state: FSMContext):
    kb = Keyboards()
    await msg.answer('На что хотите пожаловаться?', reply_markup=kb.report_markup())
    await state.set_state(SendReport.get_context)


@r.message(
    F.text.in_([
        Keyboards.translation.text,
        Keyboards.bug.text
    ]),
    StateFilter(SendReport.get_context)
)
async def report_translation_and_bug(msg: Message, state: FSMContext):
    await state.update_data(context=msg.text)
    await msg.answer(
        'Подробно опишите проблему, медиафайлы не принимаются, только текст',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(SendReport.get_content)


@r.message(F.text == Keyboards.promocode.text, StateFilter(SendReport.get_context))
async def report_promocode(msg: Message, state: FSMContext):
    await state.update_data(context=msg.text)
    await msg.answer(
        'Отправьте не сработавший промокод и ссылку на сайт, где вы пытались его использовать, '
        'медиафайлы не принимаются, только текст',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(SendReport.get_content)


@r.message(F.text == Keyboards.feedback.text, StateFilter(SendReport.get_context))
async def report_feedback(msg: Message, state: FSMContext):
    await state.update_data(context=msg.text)
    await msg.answer(
        'Расскажите, чем вы хотели бы поделиться, возможно, '
        'предложить идеи по доработке или просто связаться для сотрудничества',
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(SendReport.get_content)


@r.message(F.text, StateFilter(SendReport.get_content))
async def get_content(msg: Message, state: FSMContext):
    data = await state.get_data()
    conf = Config()
    kb = Keyboards()

    text = (
        f'#{data["context"]}\n'
        f'От @{msg.from_user.username}\n\n'
        f'{msg.text}'
    )

    await bot.send_message(chat_id=conf.get_report_chat(), text=text)
    await msg.answer('Отправлено, спасибо за обратную связь!', reply_markup=kb.to_menu_markup())
    await state.set_data({})
    await state.set_state(None)

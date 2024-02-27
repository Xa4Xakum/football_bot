from aiogram.fsm.state import StatesGroup, State


class AddPromo(StatesGroup):
    get_promo_text = State()
    get_ref_link = State()
    get_cite = State()
    check_correct = State()


class DeletePromo(StatesGroup):
    get_promo = State()
    confirm = State()


class Mail(StatesGroup):
    get_content = State()


class AddTranslation(StatesGroup):
    get_link = State()
    get_description = State()
    check_correct = State()


class DeleteTranslation(StatesGroup):
    get_translation_id = State()


class SendReport(StatesGroup):
    get_context = State()
    get_content = State()

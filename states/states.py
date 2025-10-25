from aiogram.fsm.state import State, StatesGroup


class PhoneAccept(StatesGroup):
    start_message = State()
    new_phone_number = State()
    change_phone_number = State()


class DepartChoice(StatesGroup):
    msg_id = State()
    dep_id = State()
    desc = State()


class AdminAct(StatesGroup):
    addremlvl1 = State()
    addremlvl2 = State()
    msg_id = State()
    phone = State()


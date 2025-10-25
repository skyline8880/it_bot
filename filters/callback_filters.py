from aiogram.filters.callback_data import CallbackData


class DepartmentsCD(CallbackData, prefix='dep'):
    depart: int
    name: str


class CancelCD(CallbackData, prefix='act'):
    cancel: str


class RequestCD(CallbackData, prefix='request_id'):
    message_id: int
    telegram_id: int
    act_id: int


class AdminCD(CallbackData, prefix='menu_act'):
    act_type: int


class AddRemoveAct(CallbackData, prefix='addrem_act'):
    act_type: int

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


class AdminMenu(CallbackData, prefix='adm_act'):
    act_type: int


class SystemServiceMenu(CallbackData, prefix='sys_id'):
    act_type: int


class BackMenu(CallbackData, prefix='back'):
    act_type: int


class ServiceActionMenu(CallbackData, prefix='serv_act'):
    act_type: int

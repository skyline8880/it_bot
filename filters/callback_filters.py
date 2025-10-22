from aiogram.filters.callback_data import CallbackData


class DepartmentsCD(CallbackData, prefix='dep'):
    depart: int
    name: str


class CancelCD(CallbackData, prefix='act'):
    cancel: str

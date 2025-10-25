from typing import Union

from aiogram.enums.chat_type import ChatType
from aiogram.enums.content_type import ContentType
from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from database.database import Database
from states.states import DepartChoice
from secrets.secrets import Secrets


class StateIsActive(Filter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        return await state.get_state()






class IsPrivate(Filter):
    async def __call__(self, message: Union[Message, CallbackQuery]) -> bool:
        if isinstance(message, CallbackQuery):
            current_chat_type = message.message.chat.type
        else:
            current_chat_type = message.chat.type
        return current_chat_type == ChatType.PRIVATE.value


class IsAdmin(Filter):
    async def __call__(self, message: Union[Message, CallbackQuery]) -> bool:
        db = Database()
        emp_data = await db.select_employee_by_sign(message.from_user.id)
        return emp_data[1]


class IsExecutor(Filter):
    async def __call__(self, message: Union[Message, CallbackQuery]) -> bool:
        db = Database()
        emp_data = await db.select_employee_by_sign(message.from_user.id)
        return emp_data[-1]


class IsDev(Filter):
    async def __call__(self, message: Union[Message, CallbackQuery]) -> bool:
        return message.from_user.id == int(Secrets.DEVELOPER)

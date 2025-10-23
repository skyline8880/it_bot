from typing import Union

from aiogram.enums.chat_type import ChatType
from aiogram.enums.content_type import ContentType
from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from database.database import Database
from states.states import DepartChoice


class CreatingRequest(Filter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        res = False
        if (await state.get_state() == DepartChoice.dep_id or 
                await state.get_state() == DepartChoice.desc):
            res = True
        return res


class IsPrivate(Filter):
    async def __call__(self, message: Union[Message, CallbackQuery]) -> bool:
        if isinstance(message, CallbackQuery):
            current_chat_type = message.message.chat.type
        else:
            current_chat_type = message.chat.type
        return current_chat_type == ChatType.PRIVATE.value

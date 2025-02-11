from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.enums.chat_type import ChatType
from aiogram.types import Message

from database.database import Database
from keyboards.auth_kbrd import get_contact_keyboard, remove_conact_keyboard
from messages.messages import accept_contact, need_auth


class UserAuthFilter(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if event.chat.type == ChatType.PRIVATE.value:
            db = Database()
            result = await db.select_employee_by_sign(
                sign=event.from_user.id)
            if event.contact is not None:
                if event.contact.user_id == event.from_user.id:
                    result = await db.insert_employee(message=event)
                    if result is not None:
                        return await event.answer(
                            text=accept_contact(),
                            reply_markup=remove_conact_keyboard)
            if result is None:
                await event.delete()
                return await event.answer(
                    text=need_auth(
                        name=event.from_user.full_name),
                    reply_markup=get_contact_keyboard)
            return await handler(event, data)

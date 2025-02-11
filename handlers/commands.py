from aiogram import Router
from aiogram.enums.chat_type import ChatType
from aiogram.enums.content_type import ContentType
from aiogram.types import Message

from bot.bot import bot
from database.database import Database
from messages.messages import (accept_request, sample_key_break,
                               sample_key_value_pair_break, sample_value_break,
                               wrong_sample)
from middleware.auth_middleware import UserAuthFilter

router = Router()
router.message.middleware(UserAuthFilter())


@router.message()
async def get_message(message: Message) -> None:
    if message.chat.type == ChatType.PRIVATE.value:
        async def sample_break_detector(message_text: str) -> list:
            db = Database()
            await db.check_updates(message=message)
            if message_text is None:
                return await message.answer(
                    text=wrong_sample())
            msg_list = message_text.split("\n")
            if len(msg_list) < 5:
                return await message.answer(
                    text=wrong_sample())
            result = []
            for index, element in enumerate(msg_list):
                if ":" not in element:
                    return await message.answer(
                        text=sample_key_value_pair_break(element=element))
                if index < 4:
                    try:
                        element, value = element.split(":")
                    except Exception:
                        return await message.answer(
                            text=sample_key_value_pair_break(element=element))
                else:
                    try:
                        desc_element = element.split(":")
                    except Exception:
                        return await message.answer(
                            text=sample_key_value_pair_break(element=element)
                        )
                element = element.strip().capitalize()
                value = value.strip().capitalize()
                if index == 0:
                    if element != "Клуб":
                        return await message.answer(
                            text=sample_key_break(
                                sample="Клуб", element=element)
                        )
                    depart = await db.select_department_by_sign(sign=value)
                    if depart is None:
                        return await message.answer(
                            text=sample_value_break(key="Клуб", value=value)
                        )
                    result.append(depart[0])
                if index == 1:
                    if element != "Этаж":
                        return await message.answer(
                            text=sample_key_break(
                                sample="Этаж", element=element)
                        )
                    floor = await db.select_floor_by_sign(sign=value)
                    if floor is None:
                        return await message.answer(
                            text=sample_value_break(key="Этаж", value=value)
                        )
                    result.append(floor[0])
                if index == 2:
                    if element != "Зона":
                        return await message.answer(
                            text=sample_key_break(
                                sample="Зона", element=element)
                        )
                    zone = await db.select_zone_by_sign(sign=value)
                    if zone is None:
                        return await message.answer(
                            text=sample_value_break(key="Зона", value=value)
                        )
                    result.append(zone[0])
                if index == 3:
                    if element != "Поломка":
                        return await message.answer(
                            text=sample_key_break(
                                sample="Поломка", element=element)
                        )
                    btype = await db.select_btype_by_sign(sign=value)
                    if btype is None:
                        return await message.answer(
                            text=sample_value_break(
                                key="Поломка", value=value)
                        )
                    result.append(btype[0])
                if index == 4:
                    if desc_element[0] != "Описание":
                        return await message.answer(
                            text=sample_key_break(
                                sample="Описание", element=element))
                    print(msg_list)
                    head_desc_list = msg_list[4].split(":")
                    if len(head_desc_list) > 1:
                        head_desc_list = " ".join(head_desc_list[1:]).strip()
                    tail_desc = " ".join(msg_list[5:]).strip()
                    result.append(f"{head_desc_list} {tail_desc}")
            return result
        text_msg = message.text
        if message.content_type != ContentType.TEXT:
            text_msg = message.caption
        request_data = await sample_break_detector(message_text=text_msg)
        if isinstance(request_data, Message):
            return
        sent = await bot.create_request(
            request_data=request_data, message=message)
        await message.reply(text=accept_request(sent=sent))

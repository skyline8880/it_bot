from typing import Any, Union

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.content_type import ContentType
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import BotCommand, CallbackQuery, Message

from database.database import Database
from keyboards.admin_kbrd import create_to_menu_button
from keyboards.request_kbrd import create_request_buttons
from messages.messages import (addremm_opreation_success, request_form,
                               required_phone, stats, undefined_phone)
from secret_data.secrets import Secrets


class ITBot(Bot):
    def __init__(
            self,
            token: str = Secrets.BOT_TOKEN,
            session: None = None,
            default: None = None,
            **kwargs: Any) -> None:
        super().__init__(
            token=token,
            session=session,
            default=default,
            kwargs=kwargs)
        self.default = DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2)

    async def command_init(self) -> None:
        await self.set_my_commands(
            commands=[
                BotCommand(
                    command='start', description='Запустить бота'),
                BotCommand(
                    command='admin', description='Панель администратора')
                ])

    async def make_insert_into_db(
            self,
            request_data: str,
            message: Message,
            desc: str,
            file_id: str = None) -> tuple:
        db = Database()
        result = await db.insert_request(
            department_id=request_data[0],
            floor_id=request_data[1],
            zone_id=request_data[2],
            btype_id=request_data[3],
            message_id=message.message_id,
            creator=message.from_user.id,
            description=desc,
            file_id=file_id
        )
        return result

    async def create_request(
            self, request_data: list, message: Message) -> bool:
        GROUPS = {
            1: Secrets.MSK_IT_GROUP,
            2: Secrets.VLK_IT_GROUP,
            3: Secrets.NKR_IT_GROUP,
            4: Secrets.BUT_IT_GROUP,
        }
        # GROUPS = {
        #     1: -1002305344615,
        #     2: -1002305344615,
        #     3: -1002305344615,
        #     4: -1002305344615,
        # }
        to_chat_id = GROUPS[request_data[0]]
        db = Database()
        match message.content_type:
            case ContentType.AUDIO:
                message_id, telegram_id = await self.make_insert_into_db(
                    request_data=request_data,
                    message=message,
                    desc=message.caption.strip(),
                    file_id=message.audio.file_id
                )
                request_data = await db.select_request_by_sign(
                    message_id=message_id, telegram_id=telegram_id)
                await self.send_audio(
                    chat_id=to_chat_id,
                    audio=request_data[18],
                    caption=request_form(data=request_data),
                    reply_markup=await create_request_buttons(
                        message_id=message_id,
                        telegram_id=telegram_id,
                        status_id=request_data[19]
                    )
                )
            case ContentType.DOCUMENT:
                message_id, telegram_id = await self.make_insert_into_db(
                    request_data=request_data,
                    message=message,
                    desc=message.caption.strip(),
                    file_id=message.document.file_id
                )
                request_data = await db.select_request_by_sign(
                    message_id=message_id, telegram_id=telegram_id)
                await self.send_document(
                    chat_id=to_chat_id,
                    document=request_data[18],
                    caption=request_form(data=request_data),
                    reply_markup=await create_request_buttons(
                        message_id=message_id,
                        telegram_id=telegram_id,
                        status_id=request_data[19]
                    )
                )
            case ContentType.PHOTO:
                message_id, telegram_id = await self.make_insert_into_db(
                    request_data=request_data,
                    message=message,
                    desc=message.caption.strip(),
                    file_id=message.photo[-1].file_id
                )
                request_data = await db.select_request_by_sign(
                    message_id=message_id, telegram_id=telegram_id)
                await self.send_photo(
                    chat_id=to_chat_id,
                    photo=request_data[18],
                    caption=request_form(data=request_data),
                    reply_markup=await create_request_buttons(
                        message_id=message_id,
                        telegram_id=telegram_id,
                        status_id=request_data[19]
                    )
                )
            case ContentType.VIDEO:
                message_id, telegram_id = await self.make_insert_into_db(
                    request_data=request_data,
                    message=message,
                    desc=message.caption.strip(),
                    file_id=message.video.file_id
                )
                request_data = await db.select_request_by_sign(
                    message_id=message_id, telegram_id=telegram_id)
                await self.send_video(
                    chat_id=to_chat_id,
                    video=request_data[18],
                    caption=request_form(data=request_data),
                    reply_markup=await create_request_buttons(
                        message_id=message_id,
                        telegram_id=telegram_id,
                        status_id=request_data[19]
                    )
                )
            case ContentType.VOICE:
                message_id, telegram_id = await self.make_insert_into_db(
                    request_data=request_data,
                    message=message,
                    desc=message.caption.strip(),
                    file_id=message.voice.file_id
                )
                request_data = await db.select_request_by_sign(
                    message_id=message_id, telegram_id=telegram_id)
                await self.send_voice(
                    chat_id=to_chat_id,
                    voice=request_data[18],
                    caption=request_form(data=request_data),
                    reply_markup=await create_request_buttons(
                        message_id=message_id,
                        telegram_id=telegram_id,
                        status_id=request_data[19]
                    )
                )
            case ContentType.TEXT:
                message_id, telegram_id = await self.make_insert_into_db(
                    request_data=request_data,
                    message=message,
                    desc=message.text.strip(),
                )
                request_data = await db.select_request_by_sign(
                    message_id=message_id, telegram_id=telegram_id)
                await self.send_message(
                    chat_id=to_chat_id,
                    text=request_form(request_data),
                    reply_markup=await create_request_buttons(
                        message_id=message_id,
                        telegram_id=telegram_id,
                        status_id=request_data[19]
                    )
                )
            case _:
                await message.delete()
                return False
        return True

    async def update_request(
            self,
            act_id: Union[int, str],
            message_id: Union[int, str],
            telegram_id: Union[int, str],
            query: CallbackQuery) -> bool:
        db = Database()
        await db.update_request(
            status_id=int(act_id),
            executor_id=query.from_user.id,
            message_id=int(message_id),
            telegram_id=int(telegram_id)
        )
        request_data = await db.select_request_by_sign(
            message_id=message_id, telegram_id=telegram_id)
        chat_id = query.message.chat.id
        chat_message_id = query.message.message_id
        if query.message.content_type == ContentType.TEXT.value:
            await self.edit_message_text(
                text=request_form(request_data),
                chat_id=chat_id,
                message_id=chat_message_id,
                reply_markup=await create_request_buttons(
                    message_id=message_id,
                    telegram_id=telegram_id,
                    status_id=int(act_id),
                )
            )
        else:
            await self.edit_message_caption(
                caption=request_form(request_data),
                chat_id=chat_id,
                message_id=chat_message_id,
                reply_markup=await create_request_buttons(
                    message_id=message_id,
                    telegram_id=telegram_id,
                    status_id=int(act_id),
                )
            )

    async def update_admin_or_executor(
            self,
            addremlvl1: Union[int, str],
            addremlvl2: Union[int, str],
            message: Message) -> bool:
        success = False
        if message.content_type != ContentType.TEXT.value:
            return success, required_phone()
        phone = message.text.strip()
        db = Database()
        employee = await db.select_employee_by_sign(sign=phone)
        if not employee:
            return success, undefined_phone()
        success = True
        add = True if int(addremlvl2) == 1 else False
        if int(addremlvl1) == 1:
            result = await db.update_is_admin(
                phone=phone,
                is_admin=add,
                is_executor=add
            )
        elif int(addremlvl1) == 2:
            result = await db.update_is_executor(
                phone=phone,
                is_executor=add
            )
        print(result.statusmessage)
        return success, addremm_opreation_success(
            act_lvl1=addremlvl1, act_lvl2=addremlvl2, phone=phone)

    async def open_stats(self, query: CallbackQuery):
        db = Database()
        result = await db.select_requests_stats()
        await query.message.answer(
            text=stats(result),
            reply_markup=await create_to_menu_button())


bot = ITBot()

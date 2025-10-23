from secrets.secrets import Secrets
from typing import Any

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.content_type import ContentType
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import BotCommand, Message

from database.database import Database
from messages.messages import request_form


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
                BotCommand(command='start', description='Запустить бота')])

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
        #GROUPS = {
        #    1: Secrets.MSK_IT_GROUP,
        #    2: Secrets.VLK_IT_GROUP,
        #    3: Secrets.NKR_IT_GROUP,
        #    4: Secrets.BUT_IT_GROUP,
        #}
        GROUPS = {
            1: -1002305344615,
            2: -1002305344615,
            3: -1002305344615,
            4: -1002305344615,
        }
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
                    audio=request_data[-1],
                    caption=request_form(data=request_data)
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
                    document=request_data[-1],
                    caption=request_form(data=request_data)
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
                    photo=request_data[-1],
                    caption=request_form(data=request_data)
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
                    video=request_data[-1],
                    caption=request_form(data=request_data)
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
                    voice=request_data[-1],
                    caption=request_form(data=request_data)
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
                    text=request_form(request_data)
                )
            case _:
                await message.delete()
                return False
        return True


bot = ITBot()

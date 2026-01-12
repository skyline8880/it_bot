from aiogram import Router
from aiogram.enums.content_type import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.bot import bot

router = Router()


@router.message()
async def handle_private_message(message: Message, state: FSMContext):
    replied = message.reply_to_message
    if replied:
        replied_text = replied.text
        if replied.content_type != ContentType.TEXT:
            replied_text = replied.caption
        print(replied_text, bot)
    # msg_data = re.findall(
    #     pattern=r'\b(\D+)\s(\d+)/(-\d+|\d+)\b',
    #     string=replied_text)
    # if not msg_data:
    #     return

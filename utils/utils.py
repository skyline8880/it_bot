from aiogram.enums import ParseMode
from aiogram.utils.text_decorations import html_decoration as hd
from telegram.error import TelegramError

from bot.bot import bot


async def safe_send_message(chat_id: int, text: str, **kwargs) -> bool:

    try:
        await bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=ParseMode.HTML,
            **kwargs
        )
        return True
    except TelegramError as e:
        print(f"Format error: {e}")
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=hd.quote(text),
                parse_mode=None,
                **kwargs
            )
            return True
        except Exception as fallback_error:
            print(f"Fallback error: {fallback_error}")
            return False

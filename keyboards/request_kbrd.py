from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from filters.callback_filters import RequestCD


async def create_request_buttons(
        message_id, telegram_id, status_id):
    button_text, act_id = (
        ["Завершить", 3] if status_id == 2 else ["Взять в работу", 2])
    return InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=button_text,
                    callback_data=RequestCD(
                        message_id=message_id,
                        telegram_id=telegram_id,
                        act_id=act_id).pack())
            ]
        ])

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from filters.callback_filters import DepartmentsCD, CancelCD
from database.database import Database


cancel_button = [
    InlineKeyboardButton(
        text="Отмена",
        callback_data=CancelCD(
            cancel="cancel").pack())
]

async def create_cancel_button():
    return InlineKeyboardMarkup(
        row_width=1, 
        inline_keyboard=[
            cancel_button
        ])

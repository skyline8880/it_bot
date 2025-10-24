from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from filters.callback_filters import DepartmentsCD, CancelCD
from database.database import Database

async def create_cancel_button():
    return InlineKeyboardMarkup(
        row_width=1, 
        inline_keyboard=[
            [
            InlineKeyboardButton(
                text="Отменить заявку",
                callback_data=CancelCD(
                    cancel="cancel").pack())
            ]
        ])

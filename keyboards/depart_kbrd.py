from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from filters.callback_filters import DepartmentsCD
from database.database import Database

async def create_depart_buttons():
    db = Database()
    departs = await db.select_departments()
    depart_name_buttons = []
    for dep_id, dep_name in departs:
        depart_name_buttons.append([
            InlineKeyboardButton(
                text=dep_name,
                callback_data=DepartmentsCD(
                    depart=dep_id,
                    name=dep_name).pack())
        ])
    return InlineKeyboardMarkup(
        row_width=1, inline_keyboard=depart_name_buttons)

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.database import Database
from filters.callback_filters import DepartmentsCD
from keyboards.admin_kbrd import to_menu_button


async def create_depart_buttons(is_admin: bool = False):
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
    if is_admin:
        depart_name_buttons.append(to_menu_button)
    return InlineKeyboardMarkup(
        row_width=1, inline_keyboard=depart_name_buttons)

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from filters.callback_filters import AddRemoveAct, AdminCD, AdminMenu

to_menu_button = [
    InlineKeyboardButton(
                text="Меню",
                callback_data=AdminMenu(
                    act_type=1).pack())
]


async def create_admin_buttons():
    buttons = []
    for button_text, act_type in [
            ["Администраторы", 1],
            ["Специалисты", 2],
            ["Создать заявку", 3],
            ["Статистика", 4]]:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=button_text,
                    callback_data=AdminCD(
                        act_type=act_type).pack())
            ]
        )
    return InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=buttons)


async def create_addremove_buttons():
    buttons = []
    for button_text, act_type in [["Добавить", 1], ["Удалить", 2]]:
        buttons.append(
            InlineKeyboardButton(
                text=button_text,
                callback_data=AddRemoveAct(
                    act_type=act_type).pack())
        )
    return InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            buttons,
            to_menu_button
        ])


async def create_to_menu_button():
    return InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            to_menu_button
        ])

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from filters.callback_filters import (AddRemoveAct, AdminCD, AdminMenu,
                                      BackMenu, ServiceActionMenu,
                                      SystemServiceMenu)

to_menu_button = [
    InlineKeyboardButton(
                text="Меню",
                callback_data=AdminMenu(
                    act_type=1).pack())
]


back_button = [
    InlineKeyboardButton(
                text="Назад",
                callback_data=BackMenu(
                    act_type=-1).pack())
]


async def create_admin_buttons():
    buttons = []
    for button_text, act_type in [
            ["Администраторы", 1],
            ["Специалисты", 2],
            ["Создать заявку", 3],
            ["Статистика", 4],
            ["Проверка служб", 5]]:
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


async def create_system_services_button():
    buttons_ = []
    buttons = []
    cnt = 1
    for button_text, act_type in [
        ["CRAFT - МСК", 1],
        ["CRAFT - ВЛК", 2],
        ["CRAFT - НКР", 3],
        ["CRAFT - БУН", 4],
        # ["AVI - МСК", 5],
        # ["AVI - ВЛК", 6],
        # ["AVI - НКР", 7],
        # ["AVI - БУН", 8],
    ]:
        buttons.append(
            InlineKeyboardButton(
                text=button_text,
                callback_data=SystemServiceMenu(
                    act_type=act_type).pack())
        )
        cnt += 1
        if cnt == 3:
            buttons_.append(buttons)
            buttons = []
            cnt = 1
    buttons_.append(to_menu_button)
    return InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=buttons_)


async def create_back_button():
    return InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            back_button
        ])


async def create_service_actions_button():
    buttons = []
    for button_text, act_type in [
            ["Проверить", 1],
            ["Перезапустить", 2]]:
        buttons.append(
            InlineKeyboardButton(
                text=button_text,
                callback_data=ServiceActionMenu(
                    act_type=act_type).pack())
        )
    return InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            buttons,
            back_button
        ])

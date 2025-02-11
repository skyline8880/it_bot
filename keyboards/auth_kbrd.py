from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)

get_contact_button = KeyboardButton(
    text='Отправить контакт', request_contact=True)
cancel_contact_button = KeyboardButton(
    text='Отменить операцию')
get_contact_keyboard = ReplyKeyboardMarkup(
    keyboard=[[get_contact_button]],
    resize_keyboard=True,
    one_time_keyboard=True)
change_contact_keyboard = ReplyKeyboardMarkup(
    keyboard=[[get_contact_button, cancel_contact_button]],
    resize_keyboard=True,
    one_time_keyboard=True)
remove_conact_keyboard = ReplyKeyboardRemove()

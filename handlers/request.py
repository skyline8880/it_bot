from secrets.secrets import Secrets
from urllib.parse import unquote
from filters.callback_filters import DepartmentsCD, CancelCD
from aiogram import F, Router
from bot.bot import bot
from aiogram.enums import ChatType, ContentType
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message, CallbackQuery
from cachetools import TTLCache
from states.states import DepartChoice
from aiogram.fsm.context import FSMContext
from keyboards.depart_kbrd import create_depart_buttons
from keyboards.cancel_kdrd import create_cancel_button
from bot.bot import ITBot
from database.database import Database
from messages.messages import (invalid_qr_format, now_description_message,
                               processing_error, request_cancelled,
                               request_error, request_sent_success,
                               scan_qr_message, start_instruction,
                               wrong_sample, start_menu, detail_desc)
from middleware.auth_middleware import UserAuthFilter


router = Router()
router.message.middleware(UserAuthFilter())


@router.callback_query(DepartmentsCD.filter())
async def start_cmd(query: CallbackQuery, state: FSMContext):
    _, dep_id, dep_name = query.data.split(':')
    await state.update_data(dep_id=dep_id)
    await state.set_state(DepartChoice.desc)
    await query.message.delete()
    msg = await query.message.answer(
        text=detail_desc(dep_name=dep_name),
        reply_markup=await create_cancel_button()
    )
    await state.update_data(msg_id=msg.message_id)


@router.message(DepartChoice.dep_id)
async def start_cmd(message: Message, state: FSMContext):
    await message.delete()


@router.message(DepartChoice.desc)
async def start_cmd(message: Message, state: FSMContext):
    data = await state.get_data()
    await bot.delete_message(chat_id=message.chat.id, message_id=int(data['msg_id']))
    print(await state.get_data())
    print(message.content_type)
    await message.reply(text='Request Accepted')


@router.callback_query(CancelCD.filter())
async def start_cmd(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.delete()
    await query.message.answer(request_cancelled())

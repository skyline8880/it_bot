from aiogram import Router
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.bot import bot
from filters.callback_filters import CancelCD, DepartmentsCD, RequestCD
from filters.filters import IsDev, IsExecutor, IsPrivate
from keyboards.cancel_kbrd import create_cancel_button
from messages.messages import (detail_desc, operation_cancelled, request_error,
                               request_sent_success)
from states.states import DepartChoice

router = Router()


@router.callback_query(DepartmentsCD.filter(), IsPrivate())
async def get_request_description(query: CallbackQuery, state: FSMContext):
    _, dep_id, dep_name = query.data.split(':')
    await state.update_data(dep_id=dep_id)
    await state.set_state(DepartChoice.desc)
    await query.message.delete()
    msg = await query.message.answer(
        text=detail_desc(dep_name=dep_name),
        reply_markup=await create_cancel_button()
    )
    await state.update_data(msg_id=msg.message_id)


@router.message(DepartChoice.dep_id, IsPrivate())
async def ignore_messages_on_depat_choice(message: Message, state: FSMContext):
    await message.delete()


@router.message(DepartChoice.desc, IsPrivate())
async def create_request(message: Message, state: FSMContext):
    data = await state.get_data()
    await bot.delete_message(
        chat_id=message.chat.id, message_id=int(data['msg_id']))
    request_data = [int(data['dep_id']), -1, -1, -1,]
    success = await bot.create_request(request_data, message)
    if success:
        await message.reply(request_sent_success())
    else:
        await message.reply(request_error())


@router.callback_query(CancelCD.filter(), IsPrivate())
async def cancel_creating_request(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.delete()
    await query.message.answer(operation_cancelled())


@router.callback_query(
    RequestCD.filter(), or_f(IsExecutor(), IsDev()))
async def executor_request_act(query: CallbackQuery, state: FSMContext):
    _, message_id, telegram_id, act_id = query.data.split(":")
    ACTS = {
        2: "В работе",
        3: "Завершен"
    }
    await query.answer(ACTS[int(act_id)])
    await bot.update_request(
        act_id=act_id,
        message_id=message_id,
        telegram_id=telegram_id,
        query=query)


@router.callback_query(RequestCD.filter(), ~IsExecutor())
async def non_executor_request_act(query: CallbackQuery, state: FSMContext):
    await query.answer("У вас нет привилегии")

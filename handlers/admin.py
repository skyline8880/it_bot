from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.bot import bot
from filters.callback_filters import AddRemoveAct, AdminCD, AdminMenu
from filters.filters import IsPrivate
from keyboards.admin_kbrd import create_addremove_buttons, create_admin_buttons
from keyboards.cancel_kbrd import create_cancel_button
from keyboards.depart_kbrd import create_depart_buttons
from messages.messages import (admin_menu, admin_or_executor_menu,
                               enter_phone_menu, start_menu)
from states.states import AdminAct, DepartChoice

router = Router()


@router.callback_query(AdminCD.filter())
async def admin_act(query: CallbackQuery, state: FSMContext):
    _, act_id = query.data.split(':')
    if int(act_id) == 3:
        await query.message.delete()
        await state.set_state(DepartChoice.dep_id)
        return await query.message.answer(
            text=start_menu(),
            reply_markup=await create_depart_buttons(is_admin=True)
        )
    elif int(act_id) == 4:
        return await bot.open_stats(query=query)
    await state.set_state(AdminAct.addremlvl1)
    await state.update_data(addremlvl1=act_id)
    await state.set_state(AdminAct.addremlvl2)
    await query.message.delete()
    await query.message.answer(
        text=admin_or_executor_menu(act_id),
        reply_markup=await create_addremove_buttons()
    )


@router.callback_query(AddRemoveAct.filter())
async def admin_addrem_act(query: CallbackQuery, state: FSMContext):
    _, act_id = query.data.split(':')
    await state.set_state(AdminAct.addremlvl2)
    await state.update_data(addremlvl2=act_id)
    await query.message.delete()
    data = await state.get_data()
    msg = await query.message.answer(
        text=enter_phone_menu(
            act_lvl1=data["addremlvl1"], act_lvl2=act_id),
        reply_markup=await create_cancel_button()
    )
    await state.set_state(AdminAct.msg_id)
    await state.update_data(msg_id=msg.message_id)
    await state.set_state(AdminAct.phone)


@router.callback_query(AdminMenu.filter())
async def to_admin_menu_act(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.delete()
    await query.message.answer(
        text=admin_menu(),
        reply_markup=await create_admin_buttons())


@router.message(AdminAct.phone)
async def get_phone_to_act(message: Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data["msg_id"]
    success, msg = await bot.update_admin_or_executor(
        addremlvl1=data["addremlvl1"],
        addremlvl2=data["addremlvl2"],
        message=message)
    if not success:
        return await message.reply(text=msg)
    await bot.delete_message(chat_id=message.chat.id, message_id=int(msg_id))
    await message.reply(text=msg)


@router.message(IsPrivate())
async def handle_message(message: Message, state: FSMContext):
    await message.delete()

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.bot import bot
from craft.api import CraftPocket
from craft.host import RemoteServer
from filters.callback_filters import (AddRemoveAct, AdminCD, AdminMenu,
                                      BackMenu, ServiceActionMenu,
                                      SystemServiceMenu)
from filters.filters import IsPrivate
from keyboards.admin_kbrd import (create_addremove_buttons,
                                  create_admin_buttons,
                                  create_service_actions_button,
                                  create_system_services_button)
from keyboards.cancel_kbrd import create_cancel_button
from keyboards.depart_kbrd import create_depart_buttons
from messages.messages import (admin_menu, admin_or_executor_menu,
                               enter_phone_menu, start_menu)
from states.states import AdminAct, DepartChoice

router = Router()


@router.callback_query(AdminCD.filter())
async def admin_act(query: CallbackQuery, state: FSMContext):
    _, act_id = query.data.split(':')
    await state.set_state(AdminAct.addremlvl1)
    await state.update_data(addremlvl1=act_id)
    await query.message.delete()
    if int(act_id) == 3:
        await state.set_state(DepartChoice.dep_id)
        return await query.message.answer(
            text=start_menu(),
            reply_markup=await create_depart_buttons(is_admin=True)
        )
    elif int(act_id) == 4:
        return await bot.open_stats(query=query)
    elif int(act_id) == 5:
        await state.set_state(AdminAct.addremlvl2)
        return await query.message.answer(
            text="choose service",
            reply_markup=await create_system_services_button()
        )
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


@router.callback_query(BackMenu.filter())
async def back_act(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    if not await state.get_state():
        query.answer("Меню")
        return await query.answermessage.answer(
                text=admin_menu(),
                reply_markup=await create_admin_buttons())
    await query.answer("Назад")
    data = await state.get_data()
    act_id = int(data["addremlvl1"])
    if act_id == 5:
        return await query.message.answer(
            text="Выберите службу",
            reply_markup=await create_system_services_button())


@router.callback_query(SystemServiceMenu.filter())
async def choose_service_act(query: CallbackQuery, state: FSMContext):
    _, sys_id = query.data.split(":")
    if int(sys_id) > 4 or int(sys_id) < 2:
        return await query.answer("Сервис недоступен")
    await query.answer("Выбрано")
    await query.message.delete()
    await state.update_data(addremlvl2=sys_id)
    await query.message.answer(
        text="Выберите действие",
        reply_markup=await create_service_actions_button()
    )


@router.callback_query(ServiceActionMenu.filter())
async def service_act(query: CallbackQuery, state: FSMContext):
    await query.answer("Выполняю")
    _, act_id = query.data.split(":")
    data = await state.get_data()
    await query.message.delete()
    SERVICES = {
        1: [2, None, None, 2967794077],
        2: [3, 3303, 2, 2967794077],
        3: [4, 404, 2, 2967794077],
        4: [5, 502, 2, 2967794077],
        5: [2, None, None, None],
        6: [3, None, None, None],
        7: [4, None, None, None],
        8: [4, None, None, None],
    }
    lvl = int(data["addremlvl2"])
    if lvl < 5:
        dep_id, point, act_type, card_number = SERVICES[lvl]
        if int(act_id) == 1:
            craft_pocket = CraftPocket(
                dep_id=dep_id,
                query=query)
            await craft_pocket.terminals()
            await craft_pocket.pass_request(
                point=point, act_type=act_type, card_number=card_number)
        else:
            host = RemoteServer(dep_id=dep_id, query=query)
            await host.start_or_stop_service(
                service_name=host.service, type_act="stop")
            await host.start_or_stop_service(
                service_name=host.service)
    await query.message.answer(
        text="Выберите действие",
        reply_markup=await create_service_actions_button()
    )


@router.message(IsPrivate())
async def handle_message(message: Message, state: FSMContext):
    await message.delete()

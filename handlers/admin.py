import datetime as dt
import re

from aiogram import Router
from aiogram.enums.chat_action import ChatAction
from aiogram.enums.content_type import ContentType
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile, Message

from bot.bot import bot
from craft.api import CraftPocket
from craft.host import RemoteServer
from database.database import Database
from filters.callback_filters import (AddRemoveAct, AdminCD, AdminMenu,
                                      BackMenu, ReportRequestPeriod,
                                      ReportRequestStatus, ServiceActionMenu,
                                      SystemServiceMenu)
from filters.filters import IsAdmin, IsDev, IsPrivate
from keyboards.admin_kbrd import (create_addremove_buttons,
                                  create_admin_buttons, create_period_button,
                                  create_service_actions_button,
                                  create_status_button,
                                  create_system_services_button)
from keyboards.cancel_kbrd import create_cancel_button
from keyboards.depart_kbrd import create_depart_buttons
from messages.messages import (admin_menu, admin_or_executor_menu,
                               enter_phone_menu, start_menu)
from states.states import AdminAct, DepartChoice, ReportAct

router = Router()


@router.callback_query(
    AdminCD.filter(), or_f(IsAdmin(), IsDev()), IsPrivate())
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
            text="Выберите службу",
            reply_markup=await create_system_services_button()
        )
    elif int(act_id) == 6:
        return await query.message.answer(
            text="Выберите период",
            reply_markup=await create_period_button()
        )
    db = Database()
    await state.set_state(AdminAct.addremlvl2)
    custom_list = await db.select_admins_or_executors(act=int(act_id))
    await query.message.answer(
        text=admin_or_executor_menu(act_id, custom_list),
        reply_markup=await create_addremove_buttons()
    )


@router.callback_query(
    AddRemoveAct.filter(), or_f(IsAdmin(), IsDev()), IsPrivate())
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


@router.callback_query(
    AdminMenu.filter(), or_f(IsAdmin(), IsDev()), IsPrivate())
async def to_admin_menu_act(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.delete()
    await query.message.answer(
        text=admin_menu(),
        reply_markup=await create_admin_buttons())


@router.message(
    AdminAct.phone, or_f(IsAdmin(), IsDev()), IsPrivate())
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


@router.callback_query(
    BackMenu.filter(), or_f(IsAdmin(), IsDev()), IsPrivate())
async def back_act(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    if not await state.get_state():
        query.answer("Меню")
        return await query.message.answer(
                text=admin_menu(),
                reply_markup=await create_admin_buttons())
    await query.answer("Назад")
    data = await state.get_data()
    act_id = int(data["addremlvl1"])
    if act_id == 5:
        return await query.message.answer(
            text="Выберите службу",
            reply_markup=await create_system_services_button())


@router.callback_query(
    SystemServiceMenu.filter(), or_f(IsAdmin(), IsDev()), IsPrivate())
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


@router.callback_query(
    ServiceActionMenu.filter(), or_f(IsAdmin(), IsDev()), IsPrivate())
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


@router.callback_query(
    ReportRequestPeriod.filter(), or_f(IsAdmin(), IsDev()), IsPrivate())
async def report_period_act(query: CallbackQuery, state: FSMContext):
    await query.answer("Выполняю")
    _, act_id = query.data.split(":")
    await state.set_state(ReportAct.period)
    await state.update_data(period=act_id)
    await query.message.delete()
    if int(act_id) == 3:
        msg = await query.message.answer(
            text="Укажите период",
            reply_markup=await create_cancel_button()
        )
        await state.update_data(inputmsg=msg.message_id)
        return await state.set_state(ReportAct.prange)
    today = dt.datetime.now()
    if int(act_id) == 1:
        sdate = today.replace(day=1)
        edate = today
    elif int(act_id) == 2:
        edate = today.replace(day=1) - dt.timedelta(days=1)
        sdate = edate.replace(day=1)
    await state.update_data(prange=(sdate, edate))
    await state.set_state(ReportAct.status)
    return await query.message.answer(
        text="Выберите статус заявок",
        reply_markup=await create_status_button()
    )


@router.message(ReportAct.prange, or_f(IsAdmin(), IsDev()), IsPrivate())
async def custom_period_input(message: Message, state: FSMContext):
    if message.content_type != ContentType.TEXT.value:
        await message.delete()
        return message.answer("Введите текст")
    temp = re.findall(
        pattern=r'(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0,1,2])\.(19|20\d{2})',
        string=message.text)
    print(temp)
    if not temp or len(temp) < 2:
        return message.reply("Введите корректный формат даты")
    data = await state.get_data()
    sdate = dt.datetime(
        year=int(temp[0][-1]),
        month=int(temp[0][-2]),
        day=int(temp[0][-3]))
    edate = dt.datetime(
        year=int(temp[-1][-1]),
        month=int(temp[-1][-2]),
        day=int(temp[-1][-3]))
    print(sdate, edate)
    await state.update_data(prange=(sdate, edate))
    await state.set_state(ReportAct.status)
    try:
        await bot.delete_message(
            chat_id=message.from_user.id,
            message_id=int(data["inputmsg"])
        )
    except Exception:
        pass
    return await message.answer(
        text="Выберите статус заявок",
        reply_markup=await create_status_button()
    )


@router.callback_query(
    ReportRequestStatus.filter(), or_f(IsAdmin(), IsDev()), IsPrivate())
async def report_status_act(query: CallbackQuery, state: FSMContext):
    await query.answer("Выполняю")
    _, act_id = query.data.split(":")
    await state.update_data(status=act_id)
    await query.message.delete()
    db = Database()
    data = await state.get_data()
    sdate, edate = data["prange"]
    fullpath, filename = await db.select_custom_requests(
        status_id=int(data["status"]),
        department_id=0,
        sdate=sdate,
        edate=edate
    )
    await query.answer('Отчёт формируется')
    await bot.send_chat_action(
        chat_id=query.message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT
    )
    await bot.send_document(
        chat_id=query.message.chat.id,
        document=FSInputFile(path=fullpath, filename=filename),
        caption="Отчет готов")


@router.message(IsPrivate())
async def handle_message(message: Message, state: FSMContext):
    await message.delete()

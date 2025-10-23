from secrets.secrets import Secrets
from urllib.parse import unquote
from filters.filters import CreatingRequest, IsPrivate
from aiogram.fsm.context import FSMContext
from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message
from cachetools import TTLCache
from states.states import DepartChoice
from keyboards.depart_kbrd import create_depart_buttons
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
qr_cache = TTLCache(maxsize=1000, ttl=300)  # Хранит QR-коды 5 минут


def validate_qr_format(qr_data: str) -> bool:
    parts = qr_data.strip().split('-')
    return len(parts) == 4 and all(part.isdigit() for part in parts)


@router.message(CommandStart())
async def start_cmd(message: Message, command: CommandObject, state: FSMContext):
    await state.clear()
    if command.args:
        qr_data = unquote(command.args)
        if validate_qr_format(qr_data):
            qr_cache[message.from_user.id] = qr_data
            await message.answer(now_description_message())
        else:
            await message.answer(invalid_qr_format())
    else:
        # await message.answer(start_instruction())
        await state.set_state(DepartChoice.dep_id)
        await message.answer(
            text=start_menu(),
            reply_markup=await create_depart_buttons()
        )
        #print("start menu")


@router.message(Command("cancel"))
async def cancel_cmd(message: Message):
    qr_cache.pop(message.from_user.id, None)
    await message.answer(request_cancelled())


@router.message(F.text.contains(f'{Secrets.BOT_LINK}?text='))
async def handle_qr_url(message: Message):
    try:
        qr_data = unquote(message.text.split('text=')[1].split('%0A')[0])
        if validate_qr_format(qr_data):
            qr_cache[message.from_user.id] = qr_data
            await message.answer(now_description_message())
        else:
            await message.answer(wrong_sample())
    except Exception:
        await message.answer(wrong_sample())


@router.message(~CreatingRequest())
async def handle_private_message(message: Message, bot: ITBot):
    user_id = message.from_user.id
    if user_id not in qr_cache:
        await message.answer(scan_qr_message())
        return

    db = Database()
    try:
        qr_data = qr_cache[user_id]
        club_id, floor_id, zone_id, issue_id = qr_data.split('-')

        # Получаем данные оборудования
        club = await db.select_department_by_sign(club_id)
        floor = await db.select_floor_by_sign(floor_id)
        zone = await db.select_zone_by_sign(zone_id)
        issue = await db.select_btype_by_sign(issue_id)

        # Получаем данные сотрудника
        employee = await db.select_employee_by_sign(str(user_id))
        if not employee and message.from_user.username:
            employee = await db.select_employee_by_sign(
                message.from_user.username)

        # Формируем данные для заявки
        request_data = [
            club[0],  # department_id
            floor[0],  # floor_id
            zone[0],  # zone_id
            issue[0],  # btype_id
            message.text.strip()  # description
        ]

        # Используем метод класса ITBot для создания заявки
        success = await bot.create_request(request_data, message)

        if success:
            await message.answer(request_sent_success())
        else:
            await message.answer(request_error())

    except Exception as e:
        print(f"Ошибка: {e}")
        await message.answer(processing_error())
    finally:
        qr_cache.pop(user_id, None)

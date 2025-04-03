from urllib.parse import unquote
from aiogram import F, Router
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message
from aiogram.enums import ChatType
from cachetools import TTLCache
from database.database import Database
from bot.bot import ITBot
from secrets.secrets import Secrets
from messages.messages import (now_description_message, invalid_qr_format,
                               request_cancelled,
                               equipment_not_found,
                               profile_not_found,
                               request_sent_success,
                               request_error,
                               processing_error,
                               start_instruction,
                               scan_qr_message,
                               wrong_sample
                               )
from middleware.auth_middleware import UserAuthFilter


router = Router()
router.message.middleware(UserAuthFilter())
qr_cache = TTLCache(maxsize=1000, ttl=300)  # Хранит QR-коды 5 минут


def validate_qr_format(qr_data: str) -> bool:
    parts = qr_data.strip().split('-')
    return len(parts) == 4 and all(part.isdigit() for part in parts)


@router.message(CommandStart())
async def start_cmd(message: Message, command: CommandObject):
    if command.args:
        qr_data = unquote(command.args)
        if validate_qr_format(qr_data):
            qr_cache[message.from_user.id] = qr_data
            await message.answer(now_description_message())
        else:
            await message.answer(invalid_qr_format())
    else:
        await message.answer(start_instruction())


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


@router.message(F.chat.type == ChatType.PRIVATE, F.text)
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

        if None in (club, floor, zone, issue):
            await message.answer(equipment_not_found())
            return

        # Получаем данные сотрудника
        employee = await db.select_employee_by_sign(str(user_id))
        if not employee and message.from_user.username:
            employee = await db.select_employee_by_sign(
                message.from_user.username)

        if not employee:
            await message.answer(profile_not_found())
            return

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

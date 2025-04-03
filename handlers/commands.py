from datetime import datetime
from secrets.secrets import Secrets
from urllib.parse import unquote

from aiogram import F, Router
from aiogram.enums import ChatType
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import Message

from database.database import Database
from messages.messages import request_form, scan_qr_add_message, wrong_sample
from middleware.auth_middleware import UserAuthFilter
from utils.utils import safe_send_message

router = Router()
router.message.middleware(UserAuthFilter())
secrets = Secrets()

ADMIN_CHAT_ID = secrets.ADMINS_GROUP
user_temp_data = {}


@router.message(CommandStart())
async def start_cmd(message: Message, command: CommandObject):
    if command.args:
        await handle_qr_data(message, unquote(command.args))
    else:
        await safe_send_message(message.chat.id, scan_qr_add_message())


@router.message(Command("cancel"))
async def cancel_cmd(message: Message):
    user_temp_data.pop(message.from_user.id, None)
    await safe_send_message(message.chat.id, "Текущая заявка отменена")


async def handle_qr_data(message: Message, qr_data: str):
    parts = qr_data.strip().split('-')
    if len(parts) != 4 or not all(p.isdigit() for p in parts):
        await safe_send_message(message.chat.id, wrong_sample())
        return

    user_temp_data[message.from_user.id] = {
        'qr_data': parts,
        'step': 'wait_description'
    }
    await safe_send_message(message.chat.id, "Теперь опишите проблему:")


@router.message(F.chat.type == ChatType.PRIVATE)
async def handle_private_message(message: Message):
    user_id = message.from_user.id
    text = message.text or message.caption or ""

    if text.strip() == scan_qr_add_message():
        return

    if (user_id in user_temp_data
            and user_temp_data[user_id]['step'] == 'wait_description'):

        db = Database()
        try:
            (
                club_id,
                floor_id,
                zone_id,
                issue_id
            ) = user_temp_data[user_id]['qr_data']

            club = await db.select_department_by_sign(sign=club_id)
            floor = await db.select_floor_by_sign(sign=floor_id)
            zone = await db.select_zone_by_sign(sign=zone_id)
            issue = await db.select_btype_by_sign(sign=issue_id)

            if None in (club, floor, zone, issue):
                await message.answer("Ошибка: данные не найдены в БД")
                return

            # Получаем данные сотрудника из БД
            employee = await db.select_employee_by_sign(str(user_id))
            if not employee and message.from_user.username:
                employee = await db.select_employee_by_sign(
                    message.from_user.username)

            if not employee:
                await message.answer("❌ Ошибка: ваш профиль не найден")
                return

            # Распаковываем данные сотрудника
            (
                employee_id,
                is_admin,
                phone,
                telegram_id,
                full_name,
                db_username
            ) = employee

            # ЗАПИСЬ В БД
            await db.insert_request(
                department_id=club[0],
                floor_id=floor[0],
                zone_id=zone[0],
                btype_id=issue[0],
                message_id=message.message_id,
                creator=user_id,
                description=text.strip(),
                file_id=message.document.file_id if message.document else None
            )

            # Формируем заявку (без изменений)
            request_data = (
                None,  # request_id
                datetime.now(),  # create_date
                club[0],  # department_id
                club[1],  # department_name
                floor[0],  # floor_id
                floor[1],  # floor_name
                zone[0],  # zone_id
                zone[1],  # zone_name
                issue[0],  # btype_id
                issue[1],  # btype_name
                message.message_id,  # message_id
                user_id,  # creator
                employee_id,  # employee_id
                is_admin,  # employee_is_admin
                phone or "Не указан",  # employee_phone
                full_name or message.from_user.full_name,
                f"{db_username}" if db_username else "Не указан",
                text.strip(),  # request_description
                None  # request_file_id
            )

            request_text = request_form(request_data)

            await message.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=request_text
            )

            await message.answer("✅ Заявка успешно отправлена")

        except Exception as e:
            print(f"Ошибка при обработке заявки: {e}")
            await message.answer("❌ Ошибка при отправке заявки")
        finally:
            user_temp_data.pop(user_id, None)

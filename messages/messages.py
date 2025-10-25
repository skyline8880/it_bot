import datetime as dt

from aiogram.utils import markdown


def admin_menu():
    return markdown.text(
    markdown.markdown_decoration.quote(
        'Панель администратора'),
    sep='\n')


def admin_or_executor_menu(act_lvl1):
    position = "администратора" if int(act_lvl1) == 1 else "специалиста"
    return markdown.text(
    markdown.markdown_decoration.quote(
        f'Добавьте или удалите {position}'),
    sep='\n')


def enter_phone_menu(act_lvl1, act_lvl2):
    position = "администратора" if int(act_lvl1) == 1 else "специалиста"
    action = "добавить" if int(act_lvl2) == 1 else "удалить"
    return markdown.text(
    markdown.markdown_decoration.quote(
        f'Введите номер {position},'),
    markdown.markdown_decoration.quote(
        f'которого нужно {action}'),
    sep='\n')


def required_phone():
    return markdown.text(
    markdown.markdown_decoration.quote(
        f'Введите номер телефона!'),
    sep='\n')


def undefined_phone():
    return markdown.text(
    markdown.markdown_decoration.quote(
        f'Пользователь с данным номером отсутствует в базе!'),
    sep='\n')


def addremm_opreation_success(act_lvl1, act_lvl2, phone):
    position = "администратор" if int(act_lvl1) == 1 else "специалист"
    action = "Добавлен" if int(act_lvl2) == 1 else "Удален"
    return markdown.text(
    markdown.markdown_decoration.quote(
        f'{action} {position}'),
    markdown.text(
        markdown.markdown_decoration.quote(
            'c номером:'),
        markdown.code(phone)),
    sep='\n')


def start_menu():
    return markdown.text(
    markdown.markdown_decoration.quote(
        'Выберите клуб, в котором'),
    markdown.markdown_decoration.quote(
        'хотите создать заявку:'),
    sep='\n')


def detail_desc(dep_name: str):
    return markdown.text(
    markdown.markdown_decoration.quote(
        f'Выбран: {dep_name}.'),
    markdown.markdown_decoration.quote(
        'Подробно опишите проблему и'),
    markdown.markdown_decoration.quote(
        'и укажите где зафиксировали.'),
    sep='\n')


def now_description_message() -> str:
    return markdown.text(
        markdown.markdown_decoration.quote(
            '📝 Теперь опишите проблему:'),
        sep='\n')


def invalid_qr_format() -> str:
    return markdown.text(
        markdown.markdown_decoration.quote(
            '❌ Неверный формат QR-кода'),
        sep='\n')


def operation_cancelled() -> str:
    return markdown.text(
        markdown.markdown_decoration.quote(
            'Операция отменена'),
        sep='\n')


def request_cancelled() -> str:
    return markdown.text(
        markdown.markdown_decoration.quote(
            '❌ Текущая заявка отменена'),
        sep='\n')


def equipment_not_found() -> str:
    return markdown.text(
        markdown.markdown_decoration.quote(
            '❌ Данные оборудования не найдены'),
        sep='\n')


def profile_not_found() -> str:
    return markdown.text(
        markdown.markdown_decoration.quote(
            '❌ Ваш профиль не найден'),
        sep='\n')


def request_sent_success() -> str:
    return markdown.text(
        markdown.markdown_decoration.quote(
            '✅ Заявка успешно отправлена'),
        sep='\n')


def request_error() -> str:
    return markdown.text(
        markdown.markdown_decoration.quote(
            '❌ Ошибка при отправке заявки'),
        sep='\n')


def processing_error() -> str:
    return markdown.text(
        markdown.markdown_decoration.quote(
            '❌ Ошибка при обработке заявки'),
        sep='\n')


def start_instruction() -> str:
    return markdown.text(
        markdown.markdown_decoration.quote(
            '🔍 Для создания заявки отсканируйте QR-код.'),
        sep='\n')


def scan_qr_message() -> str:
    return markdown.text(
        markdown.markdown_decoration.quote(
            'ℹ️ Сначала отсканируйте QR-код'),
        sep='\n')


def need_auth(name) -> str:
    if name is None:
        name = "Незнакомец"
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote('Приветствую,'),
            f'{markdown.bold(name)} '),
        markdown.markdown_decoration.quote(
            'Пройдите регистрацию, отправьте свой контакт.'),
        markdown.markdown_decoration.quote(
            'Обязательно, нажмите на кнопку ниже 🔽'),
        sep='\n')


def accept_contact() -> str:
    return markdown.text(
        markdown.markdown_decoration.quote(
            'Регистрация пройдена.'),
        sep='\n')


def sample_key_break(sample: str, element: str) -> str:
    return markdown.text(
        markdown.markdown_decoration.quote(
            'Нарушен шаблон запроса!'),
        markdown.text(
            markdown.markdown_decoration.quote('Ожидает:'),
            f'{markdown.bold(sample)} '),
        markdown.text(
            markdown.markdown_decoration.quote('Передан:'),
            f'{markdown.bold(element)} '),
        markdown.text(
            markdown.markdown_decoration.quote(
                'Отсканируйте QR-код повторно.'),
            ),
        sep='\n')


def sample_value_break(key: str, value: str) -> str:
    return markdown.text(
        markdown.markdown_decoration.quote(
            ''),
        markdown.text(
            markdown.markdown_decoration.quote('Для параметра:'),
            f'{markdown.bold(key)} '),
        markdown.text(
            markdown.markdown_decoration.quote(
                'Обнаружено ошибочное значение:'),
            f'{markdown.bold(value)} '),
        markdown.text(
            markdown.markdown_decoration.quote(
                'Отсканируйте QR-код повторно.'),
            ),
        sep='\n')


def sample_key_value_pair_break(element: str) -> str:
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote(
                'Нарушено присвоение значения параметру:'),
            f'{markdown.bold(element)}'),
        markdown.text(
            markdown.markdown_decoration.quote(
                'Отсканируйте QR-код повторно.'),
            ),
        sep='\n')


def wrong_sample() -> str:
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote(
                'Запрос не по шаблону!')),
        markdown.text(
            markdown.markdown_decoration.quote(
                'Отсканируйте QR-код повторно.'),
            ),
        sep='\n')


def accept_request(sent) -> str:
    msg = markdown.text(
        markdown.markdown_decoration.quote(
            'Ваш запрос принят!'),
        sep='\n')
    if not sent:
        msg = markdown.text(
            markdown.markdown_decoration.quote(
                'Ошибка отправки запроса!'),
            sep='\n')
    return msg


def request_form(data: tuple) -> str:
    (
        request_id,
        create_date,
        department_id,
        department_name,
        floor_id,
        floor_name,
        zone_id,
        zone_name,
        btype_id,
        btype_name,
        message_id,
        creator,
        employee_id,
        employee_is_admin,
        employee_phone,
        employee_full_name,
        employee_username,
        request_description,
        request_file_id,
        status_id,
        status,
        executor_id,
        executor_is_admin,
        executor_phone,
        executor_full_name,
        executor_username
    ) = data
    req_id = f"{message_id}/{creator}"
    if employee_full_name is None:
        employee_full_name = "<Пользователь не обозначил>"
    if employee_username is None:
        employee_username = "<Пользователь не обозначил>"
    if request_description is None or request_description == "":
        request_description = "<Пользователь не оставил описание>"
    if executor_phone is None:
        executor_phone = "<Не принято в работу>"
    if executor_full_name is None:
        executor_full_name = ""
    if executor_username is None:
        executor_username = ""
    create_date = dt.datetime.strftime(create_date, format="%d.%m.%Y в %H:%M")
    STATUSES = {
        1: '⬜',
        2: '🔳',
        3: '✅'
    }
    return markdown.text(
        markdown.text(
            markdown.markdown_decoration.quote(
                f'▪️ {status} {STATUSES[status_id]}')),
        markdown.text(
            markdown.markdown_decoration.quote(
                '▪️ Запрос №:'),
            markdown.code(req_id)),
        markdown.text(
            markdown.markdown_decoration.quote(
                '▪️ Создан:'),
            markdown.bold(create_date)),
        markdown.text(
            markdown.markdown_decoration.quote(
                '▪️ Телефон:'),
            markdown.code(employee_phone)),
        markdown.text(
            markdown.markdown_decoration.quote(
                '▪️ Имя:'),
            markdown.bold(employee_full_name)),
        markdown.text(
            markdown.markdown_decoration.quote(
                '▪️ Никнейм:'),
            markdown.code(employee_username)),
        markdown.text(
            markdown.markdown_decoration.quote(
                '➖➖➖➖➖➖'),),
        markdown.text(
            markdown.markdown_decoration.quote(
                '▪️ Клуб:'),
            markdown.bold(department_name)),
        markdown.text(
            markdown.markdown_decoration.quote(
                '▪️ Этаж:'),
            markdown.bold(floor_name)),
        markdown.text(
            markdown.markdown_decoration.quote(
                '▪️ Зона:'),
            markdown.bold(zone_name)),
        markdown.text(
            markdown.markdown_decoration.quote(
                '▪️ Поломка:'),
            markdown.bold(btype_name)),
        markdown.text(
            markdown.markdown_decoration.quote(
                '➖➖➖➖➖➖'),),
        markdown.text(
            markdown.markdown_decoration.quote(
                '▪️ Описание:'),
            markdown.bold(request_description)),
        markdown.text(
            markdown.markdown_decoration.quote(
                '➖➖➖➖➖➖'),),
        markdown.text(
            markdown.markdown_decoration.quote(
                '▪️ Специалист:'),
            markdown.code(executor_phone)),
        markdown.text(
            markdown.bold(executor_full_name),
            markdown.code(executor_username)
            ),
        sep='\n')

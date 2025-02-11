from secrets.secrets import Secrets
from typing import Tuple, Union

from aiogram.types import Message
from psycopg.errors import UniqueViolation

from database.connection.connection import DBConnection
from database.queries.create import CREATE
from database.queries.insert import INSERT_INTO_EMPLOYEE, INSERT_INTO_REQUEST
from database.queries.select import (SELECT_BTYPE_BY_SIGN,
                                     SELECT_DEPARTMENT_BY_SIGN,
                                     SELECT_EMPLOYEE_BY_SIGN,
                                     SELECT_FLOOR_BY_SIGN,
                                     SELECT_REQUEST_BY_SIGN,
                                     SELECT_ZONE_BY_SIGN)
from database.queries.update import (UPDATE_EMPLOYEE_PHONE,
                                     UPDATE_EMPLOYEE_USERNAME_FULLNAME)
from database.tables.btype import Btype
from database.tables.department import Department
from database.tables.employee import Employee
from database.tables.floor import Floor
from database.tables.request import Request
from database.tables.zone import Zone


class Database():
    def __init__(self) -> None:
        self.connection = DBConnection()

    async def split_users_data(self, message: Message) -> Tuple:
        telegram_id = message.from_user.id
        username = message.from_user.username
        full_name = message.from_user.full_name
        if username is not None:
            username = f"@{username}"
        phone = None
        if message.contact is not None:
            phone = message.contact.phone_number.replace("+", "")
        return (telegram_id, username, full_name, phone)

    async def create(self) -> None:
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(CREATE)
        await con.commit()
        await con.close()
        await self.insert_default()

    async def insert_default(self) -> None:
        con = await self.connection()
        cur = con.cursor()
        for table in [Department, Floor, Zone, Btype]:
            for attr in table().__dict__:
                try:
                    await cur.execute(
                        query=f"""
                            INSERT INTO
                                {Secrets.SCHEMA_NAME}.{table()} ({table.NAME})
                            VALUES (%(attr)s)
                        """,
                        params={
                            "attr": table().__getattribute__(attr)
                        }
                    )
                    print(
                        f"Новое значение: {table().__getattribute__(attr)} "
                        f"добавлено в: {Secrets.SCHEMA_NAME}.{table()}"
                    )
                except UniqueViolation:
                    print(
                        f"В {Secrets.SCHEMA_NAME}.{table()} уже было "
                        f"добавлено: {table().__getattribute__(attr)}"
                    )
                    await con.rollback()
                except Exception as e:
                    print(
                        f"Ошибка, при добавлении в "
                        f"{Secrets.SCHEMA_NAME}.{table()}"
                        f"значения: {table().__getattribute__(attr)}\n{e}"
                    )
                    await con.rollback()
            await con.commit()
        await con.close()

    async def select_department_by_sign(self, sign: Union[int, str]) -> Tuple:
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=SELECT_DEPARTMENT_BY_SIGN,
            params={"sign": str(sign)})
        result = await cur.fetchone()
        await con.close()
        return result

    async def select_floor_by_sign(self, sign: Union[int, str]) -> Tuple:
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=SELECT_FLOOR_BY_SIGN,
            params={"sign": str(sign)})
        result = await cur.fetchone()
        await con.close()
        return result

    async def select_zone_by_sign(self, sign: Union[int, str]) -> Tuple:
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=SELECT_ZONE_BY_SIGN,
            params={"sign": str(sign)})
        result = await cur.fetchone()
        await con.close()
        return result

    async def select_btype_by_sign(self, sign: Union[int, str]) -> Tuple:
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=SELECT_BTYPE_BY_SIGN,
            params={"sign": str(sign)})
        result = await cur.fetchone()
        await con.close()
        return result

    async def select_employee_by_sign(self, sign: Union[int, str]) -> Tuple:
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=SELECT_EMPLOYEE_BY_SIGN,
            params={"sign": str(sign)})
        result = await cur.fetchone()
        await con.close()
        return result

    async def select_request_by_sign(
            self,
            message_id: Union[int, str],
            telegram_id: Union[int, str]) -> Tuple:
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=SELECT_REQUEST_BY_SIGN,
            params={
                Request().MESSAGE_ID: message_id,
                Request().CREATOR: telegram_id})
        result = await cur.fetchone()
        await con.close()
        return result

    async def insert_employee(self, message: Message) -> Tuple:
        (
            telegram_id,
            username,
            full_name,
            phone
        ) = await self.split_users_data(message=message)
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=INSERT_INTO_EMPLOYEE,
            params={
                Employee().PHONE: phone,
                Employee().TELEGRAM_ID: telegram_id,
                Employee().FULLNAME: full_name,
                Employee().USERNAME: username})
        result = await cur.fetchone()
        await con.commit()
        await con.close()
        return result

    async def insert_request(
            self,
            department_id: Union[int, str],
            floor_id: Union[int, str],
            zone_id: Union[int, str],
            btype_id: Union[int, str],
            message_id: Union[int, str],
            creator: Union[int, str],
            description: Union[int, str],
            file_id: Union[int, str, None] = None) -> Tuple:
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=INSERT_INTO_REQUEST,
            params={
                Request().DEPARTMENT_ID: department_id,
                Request().FLOOR_ID: floor_id,
                Request().ZONE_ID: zone_id,
                Request().BTYPE_ID: btype_id,
                Request().MESSAGE_ID: message_id,
                Request().CREATOR: creator,
                Request().DESCRIPTION: description,
                Request().FILEID: file_id})
        result = await cur.fetchone()
        await con.commit()
        await con.close()
        return result

    async def check_updates(self, message: Message) -> None:
        (
            telegram_id,
            username,
            full_name,
            phone
        ) = await self.split_users_data(message=message)
        employee_data = await self.select_employee_by_sign(
            sign=telegram_id)
        if phone is None:
            if employee_data[4] != full_name or employee_data[5] != username:
                con = await self.connection()
                cur = con.cursor()
                await cur.execute(
                    query=UPDATE_EMPLOYEE_USERNAME_FULLNAME,
                    params={Employee().FULLNAME: full_name,
                            Employee().USERNAME: username,
                            Employee().TELEGRAM_ID: telegram_id})
                await con.commit()
                await con.close()
                return True, False
        if telegram_id == employee_data[4]:
            con = await self.connection()
            cur = con.cursor()
            await cur.execute(
                query=UPDATE_EMPLOYEE_PHONE,
                params={Employee().PHONE: phone,
                        Employee().FULLNAME: full_name,
                        Employee().USERNAME: username,
                        Employee().TELEGRAM_ID: telegram_id})
            await con.commit()
            await con.close()
            return False, True
        return False, False

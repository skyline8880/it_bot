import datetime as dt
import os
from typing import List, Optional, Tuple, Union

import pandas as pd
from aiogram.types import Message
from psycopg.errors import UniqueViolation

from database.connection.connection import DBConnection
from database.queries.create import CREATE
from database.queries.insert import INSERT_INTO_EMPLOYEE, INSERT_INTO_REQUEST
from database.queries.select import (SELECT_ADMINS, SELECT_BTYPE_BY_SIGN,
                                     SELECT_CUSTOM_REQUESTS,
                                     SELECT_DEPARTMENT_BY_SIGN,
                                     SELECT_DEPARTMENTS,
                                     SELECT_EMPLOYEE_BY_SIGN, SELECT_EXECUTORS,
                                     SELECT_FLOOR_BY_SIGN,
                                     SELECT_REQUEST_BY_SIGN, SELECT_STATISTICS,
                                     SELECT_ZONE_BY_SIGN)
from database.queries.update import (UPDATE_EMPLOYEE_IS_ADMIN,
                                     UPDATE_EMPLOYEE_IS_EXECUTOR,
                                     UPDATE_EMPLOYEE_PHONE,
                                     UPDATE_EMPLOYEE_USERNAME_FULLNAME,
                                     UPDATE_REQUEST_STATUS_AND_EXECUTOR)
from database.tables.btype import Btype
from database.tables.department import Department
from database.tables.employee import Employee
from database.tables.floor import Floor
from database.tables.request import Request
from database.tables.status import Status
from database.tables.zone import Zone
from secret_data.secrets import Secrets


class Database():
    def __init__(self) -> None:
        self.connection = DBConnection()

    def get_connection_and_cursor(self):
        return self.connection.get_connection_and_cursor()

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
        for table in [Department, Floor, Zone, Btype, Status]:
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
            if table in (Floor, Zone, Btype):
                try:
                    await cur.execute(
                        query=f"""
                            INSERT INTO
                                {Secrets.SCHEMA_NAME}.{table()} (
                                    {table.ID}, {table.NAME})
                            VALUES (-1, 'в описании')
                        """
                    )
                    print(
                        f"Новое значение: 'в описании' "
                        f"добавлено в: {Secrets.SCHEMA_NAME}.{table()}"
                    )
                except UniqueViolation:
                    print(
                        f"В {Secrets.SCHEMA_NAME}.{table()} уже было "
                        f"добавлено: 'в описании'"
                    )
                    await con.rollback()
                except Exception as e:
                    print(
                        f"Ошибка, при добавлении в "
                        f"{Secrets.SCHEMA_NAME}.{table()}"
                        f"значения: 'в описании' {e}"
                    )
                    await con.rollback()
            await con.commit()
        await con.close()

    async def select_departments(self) -> List[Tuple[Union[int, str]]]:
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(query=SELECT_DEPARTMENTS)
        result = await cur.fetchall()
        await con.close()
        return result

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

    async def select_requests_stats(self) -> List[Tuple[str]]:
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(query=SELECT_STATISTICS)
        result = await cur.fetchall()
        await con.close()
        return result

    async def select_admins_or_executors(self, act: int) -> List[Tuple[str]]:
        query = {
            1: SELECT_ADMINS,
            2: SELECT_EXECUTORS
        }
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(query=query[act])
        result = await cur.fetchall()
        await con.close()
        return result

    # async def select_admins(self) -> List[Tuple[str]]:
    #     con = await self.connection()
    #     cur = con.cursor()
    #     await cur.execute(query=SELECT_ADMINS)
    #     result = await cur.fetchall()
    #     await con.close()
    #     return result

    # async def select_executors(self) -> List[Tuple[str]]:
    #     con = await self.connection()
    #     cur = con.cursor()
    #     await cur.execute(query=SELECT_EXECUTORS)
    #     result = await cur.fetchall()
    #     await con.close()
    #     return result

    async def select_custom_requests(
            self,
            status_id: int = 0,
            department_id: int = 0,
            sdate: Optional[dt.datetime] = None,
            edate: dt.datetime = dt.datetime.now()) -> List[Tuple[str]]:
        if not sdate:
            sdate = dt.datetime(
                year=edate.year, month=edate.month, day=edate.day)
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=SELECT_CUSTOM_REQUESTS,
            params={
                Request().STATUS_ID: status_id,
                Request().DEPARTMENT_ID: department_id,
                "sdate": sdate,
                "edate": edate
            })
        result = await cur.fetchall()
        await con.close()
        result = pd.DataFrame(
            data=result,
            columns=[
                "создан", "клуб", "этаж", "зона",
                "поломка", "номер заявки", "телефон постановщика",
                "имя постановщика", "никнейм постановщика", "описание",
                # "код файла",
                "статус", "телефон специалиста",
                "имя специалиста", "никнейм специалиста",
            ])
        styled = result.style.set_properties(**{'text-align': 'center'})
        with pd.ExcelWriter(os.path.join("reports", "Заявки.xlsx")) as writer:
            styled.to_excel(
                writer, index=False,
                sheet_name=(f'{sdate.date()} - {edate.date()}'))
            wb = writer.book
            ws = writer.sheets[f'{sdate.date()} - {edate.date()}']
            header_format = wb.add_format({
                'bold': True,
                'text_wrap': False,
                'valign': 'center',
                'align': 'center',
                'fg_color': '#f2f2e1',
                'border': 1,
                'color': '#0e0e12'})
            for col_num, value in enumerate(result.columns):
                ws.write(0, col_num, value, header_format)
                max_length = len(value) + 2
                for line in result[value]:
                    if line is not None:
                        if isinstance(line, dt.date):
                            line = dt.datetime.strftime(
                                line, '%Y-%m-%d %H:%M:%S')
                            max_length = len(line) + 2
                            break
                        if max_length < len(line):
                            max_length = len(line) + 2
                ws.set_column(col_num, col_num, max_length)
        return (
            os.path.join("reports", "Заявки.xlsx"),
            f"Заявки {sdate.date()} - {edate.date()}.xlsx")

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

    async def update_request(
            self,
            status_id: Union[int, str],
            executor_id: Union[int, str],
            message_id: Union[int, str],
            telegram_id: Union[int, str]):
        con = await self.connection()
        cur = con.cursor()
        await cur.execute(
            query=UPDATE_REQUEST_STATUS_AND_EXECUTOR,
            params={Request().STATUS_ID: status_id,
                    Request().EXECUTOR_ID: executor_id,
                    Request().MESSAGE_ID: message_id,
                    Request().CREATOR: telegram_id})
        await con.commit()
        await con.close()

    async def update_is_admin(
            self,
            phone: Union[int, str],
            is_admin: bool = True,
            is_executor: bool = True):
        con = await self.connection()
        cur = con.cursor()
        result = await cur.execute(
            query=UPDATE_EMPLOYEE_IS_ADMIN,
            params={Employee().ISADMIN: is_admin,
                    Employee().ISEXECUTOR: is_executor,
                    Employee().PHONE: phone})
        await con.commit()
        await con.close()
        return result

    async def update_is_executor(
            self,
            phone: Union[int, str],
            is_executor: bool = True):
        con = await self.connection()
        cur = con.cursor()
        result = await cur.execute(
            query=UPDATE_EMPLOYEE_IS_EXECUTOR,
            params={Employee().ISEXECUTOR: is_executor,
                    Employee().PHONE: phone})
        await con.commit()
        await con.close()
        return result

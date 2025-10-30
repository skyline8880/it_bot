import datetime as dt
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from typing import Dict, Tuple, Union

import requests
from aiogram.types import CallbackQuery
from aiogram.utils import markdown


class CraftPocket:
    PORTS = {
        2: {"port": 8082, "department": "MSK"},
        3: {"port": 8084, "department": "VLK"},
        4: {"port": 8085, "department": "NKR"},
        5: {"port": 8086, "department": "BUN"},
    }

    def __init__(
            self,
            dep_id: Union[int, str],
            query: CallbackQuery) -> None:
        self.dep_id = self._digit_check(name="dep_id", value=dep_id)
        try:
            self.port = self.PORTS[self.dep_id]["port"]
        except KeyError as keyerr:
            raise ValueError(
                f"[{dt.datetime.now()}] {self.__class__.__name__}: {keyerr}: "
                f"Wrong 'dep_id' value: '{dep_id}', "
                f"available values: {list(self.PORTS.keys())}")
        except Exception as e:
            raise Exception(
                f"[{dt.datetime.now()}] {self.__class__.__name__}: {e}")
        self.base_url = f"http://192.168.100.50:{self.port}"
        self.log_filename = os.path.join(
            os.path.join(os.path.abspath("."), "logs"),
            f"{self.PORTS[self.dep_id]['department']}-craft-pocket-test.log")
        self.craft_logger = self._setup_logger(
            logger_name=(
                f"{self.PORTS[self.dep_id]['department']}"
                "-craft-pocket-logger"),
            log_filename=self.log_filename)
        self.query = query

    def _setup_logger(
            self,
            logger_name: str,
            log_filename: str,
            level=logging.INFO) -> logging.Logger:
        file_handler = TimedRotatingFileHandler(
            filename=log_filename,
            when="midnight",
            interval=1,
            backupCount=30,
            encoding="utf-8")
        file_handler.suffix = "%Y-%m-%d"
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        logger.addHandler(file_handler)
        return logger

    def _digit_check(
            self, name: str, value: Union[int, str]) -> Union[int, float]:
        if isinstance(value, str) and not value.isdigit():
            raise ValueError(
                f"[{dt.datetime.now()}] {self.__class__.__name__}: "
                f"'{name}' value must be a digit, got: '{value}'")
        return int(value)

    def _card_fromat_check(self, name: str, value: str) -> Tuple[str, str]:
        value = str(value)
        dec_ = None
        hex_ = None
        if value.isdecimal():
            dec_ = value
            try:
                hex_ = hex(int(value))[2:].upper().zfill(8)
            except ValueError:
                raise ValueError(
                    f"[{dt.datetime.now()}] {self.__class__.__name__}: "
                    f"Can not change '{name}' decimal value: '{value}' to hex"
                    )
        else:
            dec_ = value
            try:
                if int(dec_, 16):
                    hex_ = dec_
                else:
                    raise ValueError(
                        f"[{dt.datetime.now()}] {self.__class__.__name__}: "
                        f"Wrong '{name}' hex value, got: '{value}'")
            except ValueError:
                raise ValueError(
                    f"[{dt.datetime.now()}] {self.__class__.__name__}: "
                    f"Wrong '{name}' hex value, got: '{value}'")
        return dec_, hex_

    async def _request(
            self, method: str, url: str) -> Union[
                Dict[str, Union[str, int]],
                requests.Response]:
        request_time = dt.datetime.now()
        request_message = (
            f"[{request_time}] - department: "
            f"{self.PORTS[self.dep_id]['department']} - method: "
            f"{method} - request: {url}")
        await self.query.message.answer(
            text=markdown.text(
                markdown.markdown_decoration.quote(request_message),
                sep='\n')
        )
        self.craft_logger.info(request_message)
        response = False
        try:
            response = requests.get(url)
            response_time = dt.datetime.now()
            response_message = (
                f"[{response_time}] - department: "
                f"{self.PORTS[self.dep_id]['department']} - method: "
                f"{method} - response: {response.json()}")
            await self.query.message.answer(
                text=markdown.text(
                    markdown.markdown_decoration.quote(response_message),
                    sep='\n')
            )
            empty_array = True
            tdesc = " terminals array is empty"
            if response.json() != []:
                tdesc = ""
                empty_array = False
            self.craft_logger.info(response_message)
            execution_time = response_time - request_time
            desc = " response time is too long"
            timeout = True
            if execution_time < dt.timedelta(hours=0, minutes=0, seconds=1):
                desc = ""
                timeout = False
            concat = ""
            if tdesc != "" and desc != "":
                concat = " and"
            execution_message = (
                f"[{dt.datetime.now()}] - department: "
                f"{self.PORTS[self.dep_id]['department']} - method: "
                f"{method} - execution time: "
                f"{execution_time}{desc}{concat}{tdesc}\n")
            await self.query.message.answer(
                text=markdown.text(
                    markdown.markdown_decoration.quote(execution_message),
                    sep='\n')
            )
            self.craft_logger.info(execution_message)
            err_msg = "✅Запрос отрабатывает корректно"
            if empty_array or timeout:
                err_msg = "‼️Запрос отработан со сбоем"
            await self.query.message.answer(
                text=markdown.text(
                    markdown.markdown_decoration.quote(err_msg),
                    sep='\n')
            )
        except Exception as e:
            response = False
            exception_message = (
                f"‼️‼️[{dt.datetime.now()}] - department: "
                f"{self.PORTS[self.dep_id]['department']} - method: "
                f"{method} - url: {url} - error: {e}\n")
            await self.query.message.answer(
                text=markdown.text(
                    markdown.markdown_decoration.quote(exception_message),
                    sep='\n')
            )
        return response

    async def terminals(self):
        await self.query.message.answer(
            text=markdown.text(
                markdown.markdown_decoration.quote(
                    "Выполняется запрос на список точек доступа"),
                sep='\n')
        )
        url = f"{self.base_url}/terminals"
        return await self._request(method=self.terminals.__name__, url=url)

    async def pass_request(
            self,
            point: Union[int, str],
            act_type: Union[int, str],
            card_number: str,
            role: str = "checkin"):
        await self.query.message.answer(
            text=markdown.text(
                markdown.markdown_decoration.quote(
                    "Выполняется запрос на доступ"),
                sep='\n')
        )
        point = self._digit_check(name="point", value=point)
        act_type = self._digit_check(name="act_type", value=act_type)
        dec_card, hex_card = self._card_fromat_check(
            name="card_number", value=card_number)
        input_card_message = (
            f"[{dt.datetime.now()}] - department: "
            f"{self.PORTS[self.dep_id]['department']} - method: "
            f"{self.pass_request.__name__} - read hex card number: {hex_card}"
            )
        if dec_card != hex_card:
            input_card_message = (
                f"[{dt.datetime.now()}] - department: "
                f"{self.PORTS[self.dep_id]['department']} - method: "
                f"{self.pass_request.__name__} - read decimal card number: "
                f"{dec_card} - convert decimal to hex: {hex_card}")
        await self.query.message.answer(
            text=markdown.text(
                markdown.markdown_decoration.quote(input_card_message),
                sep='\n')
        )
        self.craft_logger.info(input_card_message)
        url = (
            f"{self.base_url}/pass_request?"
            f"id={point}-{act_type}&uid={hex_card}&role={role}")
        return await self._request(method=self.pass_request.__name__, url=url)

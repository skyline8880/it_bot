import datetime as dt

import paramiko
from aiogram.types import CallbackQuery
from aiogram.utils import markdown

from secret_data.secrets import Secrets


class RemoteServer:
    SERVICE = {
        2: None,
        3: "/opt/craft_pacs/bin/craft_pacs",
        4: "/opt/craft_pacs2/bin/craft_pacs2",
        5: "/opt/craft_pacs3/bin/craft_pacs3",
    }

    def __init__(
            self,
            dep_id: int,
            query: CallbackQuery,
            host: str = Secrets.HOST,
            username: str = Secrets.HOST_USERNAME,
            password: str = Secrets.HOST_PASSWORD) -> None:
        self.host = host
        self.username = username
        self.password = password
        self.service = self.SERVICE[dep_id]
        self.query = query

    def connect_to_server(self) -> paramiko.SSHClient:
        session = paramiko.SSHClient()
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        session.connect(
            self.host,
            username=self.username,
            password=self.password,
            timeout=5.0)
        return session

    def split_response(self, command: str) -> str:
        message = None
        error = True
        try:
            session = self.connect_to_server()
            # print(f"[{dt.datetime.now()}] COMMAND: {command}")
            stdin, stdout, stderr = session.exec_command(command=command)
            # print(stdout.read().decode())
            message = (
                f"[{dt.datetime.now()}] STDOUT:"
                f"\n{stdout.read().decode(errors='ignore')}"
                )
            if stdout.channel.recv_exit_status() != 0:
                message = (
                    f"[{dt.datetime.now()}] STDERR:\n{stderr.read()}"
                    )
            stdin.close()
            stdout.close()
            stderr.close()
            session.close()
            error = False
        except TimeoutError as timerr:
            message = f"[{dt.datetime.now()}] ERROR: {timerr}"
        except Exception as e:
            message = f"[{dt.datetime.now()}] ERROR: {e}"
        finally:
            return message, error

    def get_files(
            self, remote_path: str, local_path: str, partition: str) -> None:
        try:
            session = self.connect_to_server()
            sftp = session.open_sftp()
            server_files_list = sftp.listdir(path=remote_path)
            for server_file in server_files_list:
                if partition in server_file:
                    try:
                        sftp.get(
                            f"{remote_path}"
                            f"/{server_file}",
                            localpath=(
                                f"{local_path}/{server_file}"))
                    except IOError as ioe:
                        print(ioe)
            sftp.close()
            session.close()
        except Exception as e:
            print(e)
        finally:
            print("files downloaded")

    def custom_command(self, command: str) -> str:
        return self.split_response(command=command)

    async def start_or_stop_service(
            self,
            service_name: str,
            type_act: str = "start",
            is_reverse: bool = False) -> str:
        command = f"{service_name} {type_act}"
        msg_before = (
            f"Останавливаю службу: {service_name}"
            if type_act == "stop" else f"Запускаю службу: {service_name}")
        if is_reverse:
            command = f"{type_act} {service_name}"
        await self.query.message.answer(
            text=markdown.text(
                markdown.markdown_decoration.quote(msg_before),
                sep='\n')
        )
        msg_res, error = self.split_response(command=command)
        await self.query.message.answer(
            text=markdown.text(
                markdown.markdown_decoration.quote(msg_res),
                sep='\n')
        )
        msg_after = (
            "‼️Выполнено с ошибкой"
            if error else "✅Выполнено успешно")
        await self.query.message.answer(
            text=markdown.text(
                markdown.markdown_decoration.quote(msg_after),
                sep='\n')
        )

    def grep_pin_lstart_cmd_service(self, service_name: str) -> str:
        return self.split_response(
            command=f"ps -eo pid,lstart,cmd | grep {service_name}")

    def systemctl_command(
            self,
            service_name: str,
            type_act: str = "status") -> str:
        return self.split_response(
            command=f"systemctl {type_act} {service_name}")

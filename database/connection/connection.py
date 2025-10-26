from secrets.secrets import Secrets
from typing import Tuple

import psycopg


class DBConnection():
    async def __call__(self) -> psycopg.AsyncConnection:
        self.connect = await psycopg.AsyncConnection.connect(
            host=Secrets.PGHOST,
            dbname=Secrets.PGDATABASE,
            user=Secrets.PGUSERNAME,
            password=Secrets.PGPASSWORD,
            port=Secrets.PGPORT
        )
        return self.connect

    def get_connection_and_cursor(
            self) -> Tuple[psycopg.Connection, psycopg.Cursor]:
        self.connect = psycopg.Connection.connect(
            host=Secrets.PGHOST,
            dbname=Secrets.PGDATABASE,
            user=Secrets.PGUSERNAME,
            password=Secrets.PGPASSWORD,
            port=Secrets.PGPORT
        )
        return self.connect, self.connect.cursor()

from secrets.secrets import Secrets

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

import os

from dotenv import load_dotenv

load_dotenv()


class Secrets:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    BOT_USERNAME = os.getenv("BOT_USERNAME")
    BOT_LINK = os.getenv("BOT_LINK")
    TELEGRAM_LINK = os.getenv("TELEGRAM_LINK")
    DEVELOPER = os.getenv("DEVELOPER")
    ADMINS_GROUP = os.getenv("ADMINS_GROUP")
    MSK_IT_GROUP = os.getenv("MSK_IT_GROUP")
    VLK_IT_GROUP = os.getenv("VLK_IT_GROUP")
    NKR_IT_GROUP = os.getenv("NKR_IT_GROUP")
    BUT_IT_GROUP = os.getenv("BUT_IT_GROUP")
    BOT_ID = os.getenv("BOT_ID")
    PGHOST = os.getenv('PGHOST')
    PGDATABASE = os.getenv('PGDATABASE')
    PGUSERNAME = os.getenv('PGUSERNAME')
    PGPASSWORD = os.getenv('PGPASSWORD')
    PGPORT = os.getenv('PGPORT')
    SCHEMA_NAME = os.getenv('SCHEMA_NAME')

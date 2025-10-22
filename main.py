import asyncio
import sys

from bot.bot import bot
from database.database import Database
from dispatcher.dispatcher import dp

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def main():
    db = Database()
    await db.create()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    print('bot started')


if __name__ == '__main__':
    asyncio.run(main=main())

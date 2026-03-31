import asyncio
import sys

from bot.bot import bot
from database.database import Database
from dispatcher.dispatcher import dp

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def main():
    db = Database()
    reqs = [
        [2652, 700678542],
        [2689, 1058269375],
        [2693, 1058269375],
        [2697, 1058269375],
        [2701, 1058269375],
        [2705, 1058269375],
        [2709, 1058269375],
        [4374, 333060524],
        [4382, 333060524],
        [4406, 1051610862],
        [4451, 527872708],
        [4468, 5141029832],
        [4509, 1420157979],
        #[5663, 1420157979],
        #[6197, 7357864780],
    ]
    for message_id, telegram_id in reqs:
        await db.update_request(
            status_id=3,
            executor_id=1058269375,
            message_id=message_id,
            telegram_id=telegram_id
        )


if __name__ == '__main__':
    asyncio.run(main=main())

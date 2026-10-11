import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from .config import BOT_TOKEN, DB_PATH
from .database import Database
from .handlers import router


async def run():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)
    db = Database(DB_PATH)
    await db.connect()
    try:
        await dp.start_polling(bot, db=db)
    finally:
        await db.close()


def main() -> None:
    asyncio.run(run())

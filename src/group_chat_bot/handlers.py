import logging

from aiogram import Router, Bot, F
from aiogram.enums import ChatType
from aiogram.types import Message

from .decide import should_reply
from .storage import save_message

router = Router()
logger = logging.getLogger(__name__)

router.message.filter(F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))


@router.message()
async def message_handler(message: Message, bot: Bot) -> None:
    save_message(message)

    bot_user = await bot.me()
    if should_reply(message, bot_user):
        await message.answer("Hello?")

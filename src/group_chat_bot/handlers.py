import logging

from aiogram import Router, Bot, F
from aiogram.enums import ChatType
from aiogram.types import Message, User

from .config import CONTEXT_LIMIT
from .database import Database
from .decide import should_reply
from .formatting import to_chat_message
from .llm import generate_reply

router = Router()
logger = logging.getLogger(__name__)

router.message.filter(F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))


async def reply(message: Message, bot_user: User, db: Database):
    recent_messages = await db.get_recent_messages(CONTEXT_LIMIT)
    text = await generate_reply(recent_messages, bot_user.id)

    if text:
        bot_message = await message.reply(text)
        chat_message = to_chat_message(bot_message)

        if not chat_message:
            return

        await db.add_message(chat_message)


@router.message()
async def message_handler(message: Message, bot: Bot, db: Database) -> None:
    chat_message = to_chat_message(message)
    if not chat_message:
        return

    await db.add_message(chat_message)
    bot_user = await bot.me()
    if should_reply(message, bot_user):
        await reply(message, bot_user, db)

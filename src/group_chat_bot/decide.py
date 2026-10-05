import random

from aiogram.enums import MessageEntityType
from aiogram.types import Message, User

from .config import REPLY_CHANCE


def is_addressed(message: Message, bot_user: User) -> bool:
    # TODO: add captions support
    if not message.text:
        return False

    if message.reply_to_message and message.reply_to_message.from_user:
        sender = message.reply_to_message.from_user
        if sender.id == bot_user.id:
            return True

    mention_usernames = [
        e.extract_from(message.text)[1:].lower()
        for e in message.entities or []
        if e.type == MessageEntityType.MENTION
    ]
    if bot_user.username and bot_user.username.lower() in mention_usernames:
        return True

    return False


def should_reply(message: Message, bot_user: User) -> bool:
    return is_addressed(message, bot_user) or random.random() < REPLY_CHANCE

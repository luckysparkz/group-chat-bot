from aiogram.types import Message

from .models import ChatMessage


def to_chat_message(message: Message) -> ChatMessage | None:
    sender = message.from_user
    if sender is None:
        return

    content = message.text or ""
    return ChatMessage(
        message.message_id,
        sender.id,
        sender.full_name,
        content,
        int(message.date.timestamp()),
    )

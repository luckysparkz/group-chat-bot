from aiogram.types import Message


def describe(message: Message) -> str:
    # TODO: add support for different types of messages (e.g. images, stickers)
    return f"{message.from_user}: {message.text}"


def save_message(message: Message) -> None:
    pass

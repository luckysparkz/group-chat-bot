from aiogram import html, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    name = message.from_user.full_name if message.from_user else "User"
    await message.answer(f"Hello, {html.bold(name)}!")


@router.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        message.answer("Nice try!")

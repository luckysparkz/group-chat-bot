import logging

from openai import AsyncOpenAI, APIError
from openai.types.chat import ChatCompletionMessageParam

from .config import OPENROUTER_API_KEY, MODEL
from .models import ChatMessage
from .persona import SYSTEM_PROMPT

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY
)
logger = logging.getLogger(__name__)


def build_messages(
    history: list[ChatMessage], bot_user_id: int
) -> list[ChatCompletionMessageParam]:
    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]

    for item in history:
        if item.user_id == bot_user_id:
            messages.append({"role": "assistant", "content": item.content})
        else:
            messages.append(
                {"role": "user", "content": f"{item.user_full_name}: {item.content}"}
            )

    return messages


async def generate_reply(history: list[ChatMessage], bot_user_id: int) -> str | None:
    try:
        response = await client.chat.completions.create(
            model=MODEL, messages=build_messages(history, bot_user_id)
        )
        return response.choices[0].message.content
    except APIError:
        logger.exception("Could not generate a response.")

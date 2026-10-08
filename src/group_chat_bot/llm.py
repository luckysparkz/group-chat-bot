import logging

from openai import AsyncOpenAI, APIError

from .config import OPENROUTER_API_KEY, MODEL
from .persona import SYSTEM_PROMPT

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY
)
logger = logging.getLogger(__name__)


async def generate_reply(prompt: str) -> str | None:
    try:
        response = await client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        return response.choices[0].message.content
    except APIError:
        logger.exception("Could not generate a response.")

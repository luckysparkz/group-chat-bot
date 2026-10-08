from os import getenv

from .exceptions import MissingEnvironmentVariableError

REPLY_CHANCE = 0.10
MODEL = "google/gemini-3.7-flash"


def load_env(key: str) -> str:
    value = getenv(key)

    if value is None:
        raise MissingEnvironmentVariableError(f"{key} must be defined.")

    return value


BOT_TOKEN = load_env("BOT_TOKEN")
OPENROUTER_API_KEY = load_env("OPENROUTER_API_KEY")

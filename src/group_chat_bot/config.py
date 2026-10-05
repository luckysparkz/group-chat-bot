from os import getenv

from .exceptions import MissingEnvironmentVariableError


def load_token() -> str:
    BOT_TOKEN = getenv("BOT_TOKEN")

    if BOT_TOKEN is None:
        raise MissingEnvironmentVariableError("BOT_TOKEN must be defined.")

    return BOT_TOKEN

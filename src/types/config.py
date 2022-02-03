from typing import TypedDict


class BotSection(TypedDict):
    token: str
    url: str


class Config(TypedDict):
    BOT: BotSection

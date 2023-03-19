from typing import TypedDict


class BotSection(TypedDict):
    token: str
    url: str
    owner_id: str


class Config(TypedDict):
    BOT: BotSection

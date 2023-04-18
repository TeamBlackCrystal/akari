from typing import TypedDict


class BotSection(TypedDict):
    token: str
    url: str
    owner_ids: str


class Config(TypedDict):
    BOT: BotSection

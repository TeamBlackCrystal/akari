from typing import Literal, TypedDict


class BotSection(TypedDict):
    token: str
    url: str
    owner_ids: str


class FeaturesSection(TypedDict):
    notfound_fixer: str

class JobQueueSection(TypedDict):
    type: Literal['json', 'redis']

class RedisSection(TypedDict):
    host: str
    port: int
    db: str
    password: str


class Config(TypedDict):
    BOT: BotSection
    FEATURES: FeaturesSection
    JOB_QUEUE: JobQueueSection
    REDIS: RedisSection
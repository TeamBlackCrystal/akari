from typing import TypedDict


class BotSection(TypedDict):
    token: str
    url: str
    owner_ids: str


class FeaturesSection(TypedDict):
    notfound_fixer: str

class JobQueueSection(TypedDict):
    redis_url: str


class Config(TypedDict):
    BOT: BotSection
    FEATURES: FeaturesSection
    JOB_QUEUE: JobQueueSection
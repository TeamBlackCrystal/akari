"""
AkariのConfigモデル
"""


import configparser
import json
from typing import Literal

from mipac.utils.format import remove_dict_empty


from src.types.config import Config, FeaturesSection, JobQueueSection, RedisSection


class AkariFeaturesConfig:
    def __init__(self, features_config: FeaturesSection) -> None:
        self.notfound_fixer: bool = features_config['notfound_fixer'].lower() == 'true'

class AkariJobQueueConfig:
    def __init__(self, job_queue_config: JobQueueSection) -> None:
        self.type: Literal['json', 'redis'] = job_queue_config['type']

class AkariRedisConfig:
    def __init__(self, redis_config: RedisSection) -> None:
        self.host= redis_config['host']
        self.port= redis_config['port']
        self.db = redis_config['db']
        self.password = redis_config['password'] if redis_config['password'] == '\"\"'  else None

    @property
    def to_dict(self):
        return remove_dict_empty({'host': self.host, 'port': self.port, 'db': self.db, 'password': self.password})


class AkariConfig:
    """
    Attributes
    ----------
    token : str
        Botにしたいユーザーのトークン
    url : str
        BotにしたいユーザーがいるインスタンスのURL
    """

    def __init__(self, config: Config):
        """
        Parameters
        ----------
        config: Config
            config.iniの中身
        """

        self.token: str = config['BOT']['token']
        self.url: str = config['BOT']['url']
        self.owner_ids: list[str] = json.loads(config['BOT']['owner_ids'])
        self.features: AkariFeaturesConfig = AkariFeaturesConfig(config['FEATURES'])
        self.job_queue: AkariJobQueueConfig = AkariJobQueueConfig(config['JOB_QUEUE'])
        self.redis: AkariRedisConfig = AkariRedisConfig(config['REDIS'])


config_parser = configparser.ConfigParser()
config_parser.read('./config.ini')
config = AkariConfig(config_parser.__dict__['_sections'])

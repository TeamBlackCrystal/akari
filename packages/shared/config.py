"""
AkariのConfigモデル
"""


import configparser
import json


from packages.shared.types.config import Config, FeaturesSection, JobQueueSection


class AkariFeaturesConfig:
    def __init__(self, features_config: FeaturesSection) -> None:
        self.notfound_fixer: bool = features_config['notfound_fixer'].lower() == 'true'

class AkariJobQueueConfig:
    def __init__(self, job_queue_config: JobQueueSection) -> None:
        self.redis_url: str = job_queue_config['redis_url']



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


config_parser = configparser.ConfigParser()
config_parser.read('./config.ini')
config = AkariConfig(config_parser.__dict__['_sections'])
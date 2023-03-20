"""
AkariのConfigモデル
"""


import configparser
from src.types.config import Config


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
        self.owner_id: str = config['BOT']['owner_id']


config_parser = configparser.ConfigParser()
config_parser.read('./config.ini')
config = AkariConfig(config_parser.__dict__['_sections'])

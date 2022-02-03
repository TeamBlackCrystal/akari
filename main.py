import asyncio
import configparser
from loguru import logger
from mi.ext import commands
from mi import Router, Note, User, FollowRequest

from src.models.config import AkariConfig

INITIAL_EXTENSIONS = ['src.cogs.follow']


class Akari(commands.Bot):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for cog in INITIAL_EXTENSIONS:
            self.load_extension(cog)

    async def on_ready(self, ws):
        logger.success(f'Connected {self.user.name}#{self.user.id}')
        await Router(ws).connect_channel(['main', 'home'])

    async def on_message(self, note: Note):
        logger.info(f'{note.author.name}: {note.content}')

    async def on_follow_request(self, follow_request: FollowRequest):
        logger.info(f'{follow_request.username}さんからフォローリクエストが届きました')
        await follow_request.action.accept()
        logger.success('フォローリクエストを承認しました')
        user = await follow_request.action.get_user()
        await user.action.follow.add()

    async def on_follow(self, follow: User):
        await follow.action.follow.add()


if __name__ == '__main__':
    bot = Akari()
    config_parser = configparser.ConfigParser()
    config_parser.read('./config.ini')
    config = AkariConfig(config_parser.__dict__['_sections'])

    asyncio.run(bot.start(config.url, config.token))

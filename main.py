import asyncio
from loguru import logger
from mipa.ext.commands import Bot
from mipac import (
    Note,
    NotificationFollowRequest,
    LiteUser,
    ClientManager,
    NotificationFollow,
)
from catline.adapters import QueueStorageJSONAdapter, QueueStorageRedisAdapter
from catline.queue import IFQueueStorageAdapter
from packages.shared.config import config
from packages.shared.utils.common import get_name
from src.di_container import injector

INITIAL_EXTENSIONS = [
    {'path': 'packages.bot.cogs.follow', 'is_enable': True},
    {'path': 'packages.bot.cogs.reminder', 'is_enable': True},
    {'path': 'packages.bot.cogs.notfound_fixer', 'is_enable': config.features.notfound_fixer},
]


async def follow_user(user: LiteUser, client: ClientManager):
    await user.api.follow.action.add()
    await client.note.action.send(
        visibility='specified',
        visible_user_ids=[user.id],
        content=f'{user.api.action.get_mention()} さん、よろしくね！',
    )


STRIKE = {}



class Akari(Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def connect_channel(self):
        await self.router.connect_channel(['main', 'global'])

    async def setup_hook(self) -> None:
        for cog in INITIAL_EXTENSIONS:
            if cog['is_enable']:
                await self.load_extension(cog['path'])

    async def on_reconnect(self, ws):
        logger.warning('サーバーとの接続をロストしました。再接続します。')
        await self.connect_channel()

    async def on_ready(self, ws):
        logger.success(f'Connected {get_name(self.user)}')
        await self.connect_channel()

    async def on_note(self, note: Note):
        logger.info(f'{get_name(note.author)}: {note.content}')

    async def on_follow_request(self, follow_request: NotificationFollowRequest):
        logger.info(f'{get_name(follow_request.user)}さんからフォローリクエストが届きました')
        await follow_request.user.api.follow.request.action.accept()
        logger.success('フォローリクエストを承認しました')
        await follow_user(follow_request.user, self.client)

    async def on_user_followed(self, follow: NotificationFollow):
        logger.info(f'{get_name(follow.user)}さんからフォローされました')
        await follow_user(follow.user, self.client)


async def main():
    bot = Akari()
    injector.binder.bind(IFQueueStorageAdapter, QueueStorageJSONAdapter if config.job_queue.type == 'json' else QueueStorageRedisAdapter(**config.redis.to_dict))
    
    await bot.start(config.url, config.token)

if __name__ == '__main__':
    
    asyncio.run(main())
    

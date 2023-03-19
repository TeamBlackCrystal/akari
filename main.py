import asyncio
import configparser
from loguru import logger
from mipa.ext.commands import Bot
from mipac import (
    Note,
    NotificationFollowRequest,
    LiteUser,
    ClientManager,
    NotificationFollow,
)

from src.utils.ngword import NGWordDetecter
from src.config import AkariConfig
from src.utils.common import get_name

INITIAL_EXTENSIONS = ['src.cogs.follow']


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
        for cog in INITIAL_EXTENSIONS:
            self.load_extension(cog)

    async def on_ready(self, ws):
        logger.success(f'Connected {get_name(self.user)}')
        await self.router.connect_channel(['main', 'global'])

    async def on_note(self, note: Note):
        logger.info(f'{get_name(note.author)}: {note.content}')
        if note.content:
            ng_word = await NGWordDetecter(note.content).detect()

            if ng_word['total'] > 0:
                logger.info('NG Wordに該当するノートを削除しました')
                await note.api.action.delete()
                """
                user_id: {
                "count": int,
                "reason": ["不適切な発言: 「ワード」"]
                }
                """
                current_strike = STRIKE.get(f'{note.author.id}')
                if current_strike is None:
                    current_strike = {'count': 0, 'reason': []}
                current_strike['reason'].extend(
                    [f'不適切な発言: {word}' for word in ng_word['hits']]
                )
                STRIKE[note.author.id] = {
                    'count': int(current_strike['count']) + 1,
                    'reason': current_strike['reason'],
                }

                async def send_owner(text: str):
                    await self.client.note.action.send(
                        visibility='specified',
                        visible_user_ids=[note.author.id],
                        content=text,
                    )
                note_author_mention = note.author.api.action.get_mention()
                match int(current_strike['count']):
                    case 2:
                        await send_owner(
                        f'{note_author_mention} **最終警告** 一定期間以内に複数の不適切な発言が確認されたため、次回発覚した場合アカウントが凍結されます'
                    )
                    case 3:
                        logger.info(f'{note.author.username}が3ストライクです')
                    case _: 
                        text = f'{note_author_mention} **警告** 不適切な発言が確認されたため、ノートを削除しました'
                        await send_owner(text)

    async def on_follow_request(self, follow_request: NotificationFollowRequest):
        logger.info(f'{get_name(follow_request.user)}さんからフォローリクエストが届きました')
        await follow_request.user.api.follow.request.action.accept()
        logger.success('フォローリクエストを承認しました')
        await follow_user(follow_request.user, self.client)

    async def on_user_followed(self, follow: NotificationFollow):
        logger.info(f'{get_name(follow.user)}さんからフォローされました')
        await follow_user(follow.user, self.client)


if __name__ == '__main__':
    bot = Akari()
    config_parser = configparser.ConfigParser()
    config_parser.read('./config.ini')
    config = AkariConfig(config_parser.__dict__['_sections'])

    asyncio.run(bot.start(config.url, config.token))

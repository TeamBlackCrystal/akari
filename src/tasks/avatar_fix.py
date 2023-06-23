import aiohttp
from injector import inject
from loguru import logger
from mipa.ext.commands.bot import Bot
from mipac.errors import NoSuchFileError
from urllib.parse import urlparse, parse_qs
from mipac.http import Route

from catline.queue import QueueKey, IFQueueStorageAdapter
from src.avatar_fix.avatar_fix_interface import IFAvatarFixService


def use_avatar_fix(bot: Bot):
    session = aiohttp.ClientSession()
    async def fix_notfound_image(user_id: str):
        user = await bot.client.user.action.get(user_id=user_id)
        parsed_url = urlparse(user.avatar_url)
        url_query = parse_qs(parsed_url.query)
        if isinstance(url_query, dict):
            _avatar_url = url_query.get('url')
            if _avatar_url is None:
                return  # アバターのURLが見つからない (v13より下だとなるかも)
            avatar_url = _avatar_url[0]
            logger.info(f'{user.api.action.get_mention()}の画像が使用可能か確認します')
            async with session.get(avatar_url) as resp:
                if resp.status == 404:
                    try:
                        logger.warning(f'{user.api.action.get_mention()}の画像リンクが使用できないため修復を開始します')
                        file = await bot.client.drive.file.action.show_file(url=avatar_url)
                        await bot.client.drive.file.action.remove(file.id)

                    except NoSuchFileError:
                        logger.warning('ファイルが見つかりませんでした。修復を開始します。' + avatar_url)
                    await bot.core.http.request(Route('POST', '/api/federation/update-remote-user'), json={'userId': user_id}, auth=True)
                    logger.success(f'{user.api.action.get_mention()}の画像リンクの修復が完了しました {avatar_url}')
                elif resp.status == 200:
                    logger.success(f'{user.api.action.get_mention()} のファイルに問題は見つかりませんでした {avatar_url}')
                else:
                    logger.error(f'未知の例外が発生しました: {avatar_url}, {resp.status}')
        return
                            
    return fix_notfound_image

@inject
def use_complete_avatar_fix(avatar_fix_service: IFAvatarFixService, queue_system :IFQueueStorageAdapter):
    async def complete_avatar_fix(name:str, key:QueueKey, user_id: str):
        await avatar_fix_service.complete(user_id=user_id)
        await queue_system.complete_job(name, key)
        return
    return complete_avatar_fix

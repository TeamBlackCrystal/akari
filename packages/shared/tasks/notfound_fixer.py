import aiohttp
from injector import inject
from loguru import logger
from mipa.ext.commands.bot import Bot
from mipac.errors import NoSuchFileError
from urllib.parse import urlparse, parse_qs
from mipac.http import Route

from packages.shared.adapters.redis import RedisQueueSystem
from packages.shared.interactor.notfound_fixed.complete.notfound_fixed_complete_input_if import IFNotfound_fixedCompleteInputData
from packages.shared.interactor.notfound_fixed.complete.notfound_fixed_complete_use_case import IFNotfoundFixedCompleteUseCase


def use_fix_notfound_image(bot: Bot):
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
                        await bot.client.drive.file.action.remove_file(file.id)

                    except NoSuchFileError:
                        logger.warning('ファイルが見つかりませんでした。修復を開始します。' + avatar_url)
                    await bot.core.http.request(Route('POST', '/api/federation/update-remote-user'), json={'userId': user_id}, auth=True)
                    logger.success(f'{user.api.action.get_mention()}の画像リンクの修復が完了しました')
                elif resp.status == 200:
                    logger.success(f'{user.api.action.get_mention()} のファイルに問題は見つかりませんでした')
                            
    return fix_notfound_image

@inject
def use_complete_fix_notfound_image(notfound_fixed_complete_interactor: IFNotfoundFixedCompleteUseCase, queue_system :RedisQueueSystem):
    async def complete_fix_notfound_image(key:str, user_id: str):
        await notfound_fixed_complete_interactor.handle({'user_id': user_id})
        await queue_system.complete_job(key)
    return complete_fix_notfound_image
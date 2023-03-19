from loguru import logger
from mipa import Context
from mipa.ext import commands
from mipa.ext.commands import Bot
from mipac.models import UserDetailed

from src.utils.common import get_name


class FollowManagerCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @commands.mention_command(regex=r'(.*)フォローして(.*)')
    async def follow_req(self, ctx: Context, *args):
        user = await self.bot.client.user.action.get(ctx.author.id)
        if user.is_following:
            await ctx.message.api.action.reply('既にフォローしてるよ`')
            return
        await user.api.follow.action.add()
        await ctx.message.api.action.reply(f'よろしくね、{get_name(ctx.author)}さん')

    @commands.Cog.listener() # type: ignore
    async def on_follow(self, follower: UserDetailed):
        logger.info(f'{follower.name}さんにフォローされました')


def setup(bot: Bot):
    bot.add_cog(FollowManagerCog(bot)) # type: ignore

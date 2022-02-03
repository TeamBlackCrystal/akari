from loguru import logger
from mi import Context, User
from mi.ext import commands


class FollowManagerCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.mention_command(regex=r'(.*)フォローして(.*)')
    async def follow_req(self, ctx: Context, *args):
        user = await self.bot.get_user(ctx.author.id)
        if user.is_following:
            await ctx.message.reply('既にフォローしてるよ`')
            return
        await user.action.follow.add(ctx.author.id)
        await ctx.message.reply(f'よろしくね、{ctx.author.name}さん')

    @commands.Cog.listener()
    async def on_follow(self, follower: User):
        logger.info(f'{follower.name}さんにフォローされました')


def setup(bot: commands.Bot):
    bot.add_cog(FollowManagerCog(bot))

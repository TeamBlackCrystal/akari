from mipa.ext import commands

from ..injector.di import injector


class NotFoundFixerCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(injector.create_object(NotFoundFixerCog, {'bot': bot}))

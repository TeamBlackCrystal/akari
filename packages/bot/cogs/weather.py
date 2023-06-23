from mipa.ext import commands

from packages.shared.injector.di import injector

class WeatherCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
    

async def setup(bot: commands.Bot):
    await bot.add_cog(injector.create_object(WeatherCog, {'bot': bot}))

from typing import Literal
from injector import NoInject, inject
from mipa.ext import commands
from mipa.ext.commands import Context
from mipac.models.note import Note
from src.adapters.redis import RedisQueueSystem
from src.interactor.notfound_fixed.find_by_user_id.notfound_fixed_find_by_user_id_use_case import IFNotfoundFixedFindByUserIdUseCase

from src.queue import QueueSystem
from src.tasks.notfound_fixer import use_complete_fix_notfound_image, use_fix_notfound_image

from ..injector.di import injector

current_notfound_fixer_status: Literal['running', 'stop'] = 'stop'

class NotFoundFixerCog(commands.Cog):
    @inject
    def __init__(self, bot: NoInject[commands.Bot], notfound_fixed_find_by_user_id_interactor: IFNotfoundFixedFindByUserIdUseCase) -> None:
        self.bot: commands.Bot = bot
        self.notfound_fixed_find_by_user_id_interactor = notfound_fixed_find_by_user_id_interactor
        self.queue = QueueSystem('notfound_fixer', use_fix_notfound_image(bot), success_func=injector.call_with_injection(use_complete_fix_notfound_image), queue_storage_adapter=RedisQueueSystem())
        self.queue.run()

    @commands.mention_command(regex='notfoundfixer (on|off)')
    async def trigger_notfound_fixer(self, ctx: Context, on_or_off: str):
        use_notfound_fixer = on_or_off == 'on'
        if use_notfound_fixer:
            await ctx.message.api.action.reply('画像修復機能を有効化しました。\n注意: この機能はBotを再起動すると無効になります')
            await self.queue.run()
            current_notfound_fixer_status = 'running'
        else:
            await ctx.message.api.action.reply('画像修復機能を無効化しました。')
            self.queue.stop()
            current_notfound_fixer_status = 'stop'

    @commands.Cog.listener(name='on_note')
    async def on_note(self, note: Note):
        # if current_notfound_fixer_status != 'running':
            # return
        user_id = note.author.id
        user = await self.notfound_fixed_find_by_user_id_interactor.handle({'user_id': user_id})
        if user is None:
            await self.queue.add_queue(user_id=user_id)

        
        
        
        

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(injector.create_object(NotFoundFixerCog, {'bot': bot}))

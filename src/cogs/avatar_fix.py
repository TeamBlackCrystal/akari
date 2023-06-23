from typing import Literal
from injector import NoInject, inject
from mipa.ext import commands
from mipa.ext.commands import Context
from mipac.models.note import Note
from catline.adapters import IFQueueStorageAdapter
from catline.queue import Queue

from src.tasks.avatar_fix import use_complete_avatar_fix, use_avatar_fix
from src.di_container import injector
from src.avatar_fix.avatar_fix_interface import IFAvatarFixService

current_notfound_fixer_status: Literal['running', 'stop'] = 'stop'

class NotFoundFixerCog(commands.Cog):
    @inject
    def __init__(self, bot: NoInject[commands.Bot], avatar_fix_service: IFAvatarFixService, queue_storage_adapter: IFQueueStorageAdapter) -> None:
        self.bot: commands.Bot = bot
        self.avatar_fix_service = avatar_fix_service
        self.queue = Queue('notfound_fixer', queue_storage_adapter, use_avatar_fix(bot), success_func=injector.call_with_injection(use_complete_avatar_fix),)
        self.queue.run()

    @commands.mention_command(text='fix img queue')
    async def get_fix_img_queues(self, ctx: Context):
        waiting_job = await self.queue.count_jobs('waiting')
        running_job = await self.queue.count_jobs('running')
        completed_job = await self.queue.count_jobs('completed')
        
        await ctx.message.api.action.reply(f'**IMG FIX INFO**\n待機中: {waiting_job}\n完了済み: {completed_job}\n進行中: {running_job}', visible_user_ids=[ctx.author.id])

    @commands.mention_command(regex='img fix (.*)')
    async def fix_by_id(self, ctx: Context, user_id: str):
        await self.queue.add(user_id=user_id, priority=0)
        await ctx.message.api.action.reply('画像の修復を予約しました', visible_user_ids=[ctx.author.id])

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
        user = await self.avatar_fix_service.find_by_user_id(user_id=user_id)
        if user is None:
            await self.queue.add(user_id=user_id)

        
        
        
        

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(injector.create_object(NotFoundFixerCog, {'bot': bot}))

from datetime import datetime
import random
from typing import Literal

from injector import NoInject, inject
from mipa import Context
from mipa.ext import commands
from mipa.ext.commands import Bot
from mipa.ext import tasks
from mipac.models.note import Note
from packages.shared.utils.common import get_name

from packages.shared.config import config
from src.reminder.reminder_interface import IFReminderService
from src.user.user_interface import IFUserService
from src.di_container import injector


async def enhanced_reply(note: Note, msg):
    visibility = (
        note.visibility if note.visibility in ['public', 'home'] else 'specified'
    )
    await note.api.action.reply(
        visibility=visibility, content=f'{note.author.api.action.get_mention()} {msg}',
    )


# todo: これやりましたか？でつかう
async def enhanced_quote(note: Note, msg):
    content = f'{note.author.api.action.get_mention()} {msg}'
    kwargs = {
        'visibility': note.visibility,
        'content': content,
        'visible_user_ids': [note.author.id],
    }
    if note.visibility == 'public':
        kwargs.pop('visible_user_ids')
        await note.api.action.create_quote(**kwargs)

    else:
        kwargs['visibility'] = 'specified'
        await note.api.action.reply(**kwargs)


class ReminderCog(commands.Cog):
    @inject
    def __init__(
        self,
        bot: NoInject[Bot],
        user_service: IFUserService,
        reminder_service: IFReminderService,
    ) -> None:
        self.bot = bot
        self.user_service = user_service
        self.reminder_service = reminder_service

        self.check_reminder.start()
        self.check_status.start()

    @tasks.loop(seconds=60)
    async def check_status(self):
        print('動いてるよ', datetime.now())

    @tasks.loop(seconds=21600)  # 12 * 60 * 60 (43200)
    async def check_reminder(self):
        not_done_reminders = await self.reminder_service.get_not_done_lists()
        for reminder in not_done_reminders:
            use_send = True if random.randrange(0, 4) > 2 else False
            if use_send:
                note = await self.bot.client.note.action.get(note_id=reminder.note_id)
                await enhanced_quote(note, 'これやりましたか？')

        print('これは定期メッセージです')

    @commands.mention_command(regex=r'(remind|todo) (.*)')
    async def remind(
        self,
        ctx: Context,
        remind_type: Literal['remind', 'todo'],
        title: str | None = None,
    ):
        if title is None:
            await ctx.message.api.action.reply('タイトルが指定されていないようです！')
            return

        created_user = await self.user_service.create(misskey_id=ctx.author.id)
        created_reminder = await self.reminder_service.create(title=title, note_id=ctx.message.id, user_id=created_user.misskey_id)

        await enhanced_reply(ctx.message, f'{created_reminder.title}ですね。わかりました！')

    @commands.mention_command(regex=r'(reminds|todos|tasks|タスク一覧)')
    async def todos(self, ctx: Context, arg):
        reminders = await self.reminder_service.get_lists(user_id=ctx.author.id)


        if len(reminders) > 0:
            tasks_text = '\n'.join(
                [
                    f'・[{reminder.title}]({config.url}/notes/{reminder.note_id})'
                    for reminder in reminders
                ]
            )
            print(tasks_text)
            await enhanced_reply(
                ctx.message, f'{get_name(ctx.author)}さんの{arg}です！\n{tasks_text}',
            )
        else:
            await enhanced_reply(ctx.message, '何も無いようですよ')

    @commands.mention_command(regex=r'(やった|やりました|はい|done|yes)')
    async def done(self, ctx: Context, arg):
        await enhanced_reply(ctx.message, '未実装ですよ～')

    @commands.mention_command(regex=r'(やめる|やめた|キャンセル|cancel)')
    async def cancel(self, ctx: Context, *arg):
        note = ctx.message
        reply_id = note.reply_id
        if reply_id:
            reminder = await self.reminder_service.get_by_note_id(
                note_id=reply_id
            )
            if reminder is None or ctx.message.author.id != reminder.user.misskey_id:
                await enhanced_reply(ctx.message, '見ていますからね！')
                return
            await self.reminder_service.delete(note_id=reply_id)  # 削除
            await enhanced_reply(ctx.message, 'わかったよ！また頑張ろうねッ！')
        else:
            await enhanced_reply(ctx.message, 'そっか...')


async def setup(bot: Bot):
    await bot.add_cog(
        injector.create_object(ReminderCog, additional_kwargs={'bot': bot})
    )

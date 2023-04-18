import random
from typing import Literal

from injector import NoInject, inject
from src.injector.di import injector
from mipa import Context
from mipa.ext import commands
from mipa.ext.commands import Bot
from mipa.ext import tasks
from mipac.models.note import Note
from src.interactor.reminder.delete.reminder_delete_use_case import (
    IFReminderDeleteUseCase,
)
from src.interactor.reminder.get_by_note_id.reminder_get_by_note_id_use_case import (
    IFReminderGetbynoteidUseCase,
)
from src.utils.common import get_name
from src.interactor.reminder.get_lists.reminder_get_lists_use_case import (
    IFReminderGetListsUseCase,
)
from src.interactor.reminder.get_not_done_lists.reminder_get_not_done_lists_use_case import (
    IFReminderGetnotdonelistsUseCase,
)

from src.interactor.reminder.reminder_create_use_case import IFReminderCreateUseCase
from src.interactor.user.create.user_create_use_case import IFUserCreateUseCase
from src.interactor.user.get_by_user_id.user_get_by_user_id_use_case import (
    IFUserGetbyuseridUseCase,
)

from src.config import config


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
        user_create_interactor: IFUserCreateUseCase,
        reminder_interactor: IFReminderCreateUseCase,
        user_get_by_user_id_interactor: IFUserGetbyuseridUseCase,
        reminder_get_lists_interactor: IFReminderGetListsUseCase,
        reminder_get_not_done_lists_interactor: IFReminderGetnotdonelistsUseCase,
        reminder_delete_interactor: IFReminderDeleteUseCase,
        reminder_get_by_note_interactor: IFReminderGetbynoteidUseCase,
    ) -> None:
        self.bot = bot
        self._user_create_interactor = user_create_interactor
        self._reminder_interactor = reminder_interactor
        self._user_get_by_user_id_interactor = user_get_by_user_id_interactor
        self._reminder_get_lists_interactor = reminder_get_lists_interactor
        self._reminder_get_not_done_lists_interactor = (
            reminder_get_not_done_lists_interactor
        )
        self._reminder_delete_interactor = reminder_delete_interactor
        self._reminder_get_by_note_interactor = reminder_get_by_note_interactor

        self.check_reminder.start()

    @tasks.loop(seconds=21600)  # 12 * 60 * 60 (43200)
    async def check_reminder(self):
        not_done_reminders = await self._reminder_get_not_done_lists_interactor.handle()
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

        created_user = await self._user_create_interactor.handle(
            {'misskey_id': ctx.author.id}
        )
        created_reminder = await self._reminder_interactor.handle(
            input_data={
                'note_id': ctx.message.id,
                'title': title,
                'user_id': created_user.misskey_id,
            }
        )
        await enhanced_reply(ctx.message, f'{created_reminder.title}ですね。わかりました！')

    @commands.mention_command(regex=r'(reminds|todos|tasks|タスク一覧|)')
    async def todos(self, ctx: Context, arg):

        reminders = await self._reminder_get_lists_interactor.handle(
            input_data={'user_id': ctx.author.id}
        )

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
        if note.reply:
            reply_id = note.reply_id
            reminder = await self._reminder_get_by_note_interactor.handle(
                input_data={'note_id': reply_id}
            )
            if reminder is None or ctx.message.author.id != reminder.user.misskey_id:
                await enhanced_reply(ctx.message, '見ていますからね！')
                return
            await self._reminder_delete_interactor.handle({'note_id': reply_id})  # 削除
            await enhanced_reply(ctx.message, 'わかったよ！また頑張ろうねッ！')
        else:
            await enhanced_reply(ctx.message, 'そっか...')


async def setup(bot: Bot):
    await bot.add_cog(
        injector.create_object(ReminderCog, additional_kwargs={'bot': bot})
    )

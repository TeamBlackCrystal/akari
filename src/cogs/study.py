import json
import markovify
from mipa.ext import commands
from mipac.models.note import Note

from src.mecab import mecab
from src.utils.common import check_include_url
from src.utils.ngword import IHitNGWord, detect_ng_word

NLU_DATA_FILE = 'nlu_data.json'


class StudyCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        self.wakatigaki = []
    
    @commands.Cog.listener('on_note')
    async def on_note(self, note: Note):
        content = note.content
        if content is None:
            return
        detected_ng_word: IHitNGWord = await detect_ng_word(content)
        if detected_ng_word['total'] > 0 or len(content) > 75 or await check_include_url(content):  # NG条件: NGワードが含まれる, 75文字を超える, urlが含まれる
            return
        msg = note.content
        node = mecab.parse(msg)
        self.wakatigaki.append(node)
            
        model = markovify.NewlineText('\n'.join(self.wakatigaki),state_size=3, well_formed=False)
        model = markovify.Text.from_dict(model.to_dict())
        print('自動生成: ', model.make_short_sentence(50))
            # while node:
            #     if node.surface:
            #         # 単語と品詞を取得する
            #         surface = node.surface
            #         feature = node.feature.split(',')
            #         pos = feature[0]
            #         sub_pos = feature[1]
            #         # Rasa NLUの学習データに追加する
            #         data = {
            #             "text": surface,
            #             "intent": "",
            #             "entities": [
            #                 {
            #                     "entity": "pos",
            #                     "start": 0,
            #                     "end": len(surface),
            #                     "value": pos
            #                 },
            #                 {
            #                     "entity": "sub_pos",
            #                     "start": 0,
            #                     "end": len(surface),
            #                     "value": sub_pos
            #                 }
            #             ]
            #         }
            #         add_data_to_nlu(data)
            #     node = node.next

async def setup(bot: commands.Bot):
    await bot.add_cog(StudyCog(bot))
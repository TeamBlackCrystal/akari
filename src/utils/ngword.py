from typing import TypedDict
from async_lru import alru_cache


NG_WORD_FILES = [
    'Offensive.txt',
    'Sexual_with_bopo.txt',
    'Sexual_with_mask.txt',
]
NG_WORDS = []
for ng_word_file in NG_WORD_FILES:
    with open(f'./assets/ng_words/{ng_word_file}', mode='r', encoding='utf-8') as f:
        NG_WORDS.extend([i for i in f.read().split('\n') if len(i) > 0])


class IHitNGWord(TypedDict):
    hits: list[str]
    total: int


@alru_cache(maxsize=100)
async def detect_ng_word(text: str) -> IHitNGWord:
    hits = []
    for word in NG_WORDS:
        if word in text:
            hits.append(word)
    return {'hits': hits, 'total': len(hits)}

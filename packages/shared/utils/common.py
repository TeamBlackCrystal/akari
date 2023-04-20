from mipac.models import LiteUser


def get_name(user: LiteUser):
    return user.nickname if user.nickname else user.username

async def batcher(iterable, n):
    count = 0
    result = []
    async for i in iterable:
        if n == count:
            break
        count = count+1
        result.append(i.decode('utf-8'))
        
    return result

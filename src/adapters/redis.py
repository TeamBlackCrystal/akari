import json
from src.queue import GetJobsResult, IFQueueStorageAdapter, QueueStatus, generate_queue_key
from src.redis import redis_connection
from src.utils.common import batcher


class RedisQueueSystem(IFQueueStorageAdapter):
    async def add_job(self, key: str, *args, **kwargs):
        await redis_connection.set(key, json.dumps({'args': args, 'kwargs': kwargs}))

    async def get_jobs(self, name: str, limit: int, status: QueueStatus) -> list[GetJobsResult]:
        result: list[GetJobsResult] = []
        for keybatch in await batcher(redis_connection.scan_iter(f'{status}:{name}:*'), limit):
            value = await redis_connection.get(keybatch)
            if value:  # 普通に考えればあるはず
                _value = json.loads(value)
                result.append(GetJobsResult(key=keybatch, args=_value['args'], kwargs=_value['kwargs']))  # type: ignore
        return result
    async def complete_job(self, key: str):
        ...
        # await redis_connection.delete(key)

    async def count_jobs(self, name: str, status: QueueStatus) -> int:
        count = 0
        keys = []
        async for key in redis_connection.scan_iter(f'{status}:{name}:*'):
            count = count + 1
            keys.append(key)
        return count

    async def update_status(self, key:str, name: str, status: QueueStatus) -> str:
        new_key = generate_queue_key(name, status)
        data = await redis_connection.get(key)
        await redis_connection.delete(key)
        if data is None:
            raise Exception('指定されたジョブは存在しません')
        await redis_connection.set(new_key, data)
        return new_key
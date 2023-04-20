import json
from packages.shared.queue import JOB_PRIORITIES, GetJobsResult, IFQueueStorageAdapter, JobPriority, QueueStatus, generate_queue_key
from packages.shared.redis import redis_connection
from packages.shared.utils.common import batcher


class RedisQueueSystem(IFQueueStorageAdapter):
    async def add_job(self, key: str, *args, **kwargs):
        await redis_connection.set(key, json.dumps({'args': args, 'kwargs': kwargs}))

    async def get_jobs(self, name: str, limit: int, status: QueueStatus) -> list[GetJobsResult]:
        result: list[GetJobsResult] = []
        for priority in JOB_PRIORITIES:
            if len(result) == limit:
                break
            async for _key in redis_connection.scan_iter(f'{priority}:{status}:{name}:*'):
                key = _key.decode('utf-8')
                value = await redis_connection.get(key)
                if value:  # 普通に考えればあるはず
                    _value = json.loads(value)
                    result.append(GetJobsResult(key=key, args=_value['args'], kwargs=_value['kwargs']))  # type: ignore
        return result

    async def complete_job(self, key: str):
        ...
        # await redis_connection.delete(key)

    async def count_jobs(self, name: str, status: QueueStatus) -> int:
        count = 0
        keys = []
        async for key in redis_connection.scan_iter(f'*:{status}:{name}:*'):
            count = count + 1
            keys.append(key)
        return count

    async def update_status(self, key:str, name: str, status: QueueStatus, priority: JobPriority|None=None) -> str:
        original_priority = int(key.split(':')[0])
        new_priority =  priority if priority else original_priority
        new_key = generate_queue_key(name, status, priority=new_priority)
        data = await redis_connection.get(key)
        await redis_connection.delete(key)
        if data is None:
            raise Exception('指定されたジョブは存在しません')
        await redis_connection.set(new_key, data)
        return new_key
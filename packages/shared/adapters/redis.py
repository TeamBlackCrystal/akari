import json
from packages.shared.queue import (
    JOB_PRIORITIES,
    GetJobsResult,
    IFQueueStorageAdapter,
    IJob,
    JobPriority,
    QueueKey,
    QueueStatus,
)
from packages.shared.redis import get_redis


class RedisQueueSystem(IFQueueStorageAdapter):
    def __init__(self) -> None:
        self.redis_connection = get_redis()

    async def add_job(self, key: QueueKey, *args, **kwargs):
        data: IJob = {
            "args": args,
            "identifier": key.identifier,
            "kwargs": kwargs,
            "name": key.name,
            "priority": key.priority,
            "status": key.status,
        }  # type: ignore
        await self.redis_connection.set(key.code, json.dumps(data, ensure_ascii=False))

    async def get_jobs(
        self, name: str, limit: int, status: QueueStatus
    ) -> list[GetJobsResult]:
        result: list[GetJobsResult] = []
        for priority in JOB_PRIORITIES:
            if len(result) == limit:
                break
            async for _key in self.redis_connection.scan_iter(
                f"{priority}:{status}:{name}:*"
            ):
                key = _key.decode("utf-8")
                value: str | None = await self.redis_connection.get(key)

                assert value  # 普通あるはず

                _value: IJob = json.loads(value)
                result.append(
                    GetJobsResult(
                        key=key,
                        args=_value["args"],
                        kwargs=_value["kwargs"],
                        status=_value["status"],
                        identifier=_value["identifier"],
                        priority=_value["priority"],
                    )
                )
        return result

    async def complete_job(self, name: str, key: QueueKey):
        ...
        # await redis_connection.delete(key)

    async def count_jobs(self, name: str, status: QueueStatus) -> int:
        count = 0
        keys = []
        async for key in self.redis_connection.scan_iter(f"*:{status}:{name}:*"):
            count = count + 1
            keys.append(key)
        return count

    async def update_status(
        self,
        key: QueueKey,
        name: str,
        status: QueueStatus,
        priority: JobPriority | None = None,
    ):
        new_priority = priority if priority else key.priority
        raw_data = await self.redis_connection.get(key.code)
        await self.redis_connection.delete(key.code)
        if raw_data is None:
            raise Exception(f"指定されたジョブ: {key.code} は存在しません")
        data: IJob = json.loads(raw_data)
        data["priority"] = new_priority  # type: ignore
        data["status"] = status
        await key.update(status=status, priority=new_priority)  # type: ignore
        await self.redis_connection.set(key.code, json.dumps(data, ensure_ascii=False))

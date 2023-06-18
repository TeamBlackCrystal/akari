import json
import os
from typing import Any, TypedDict
from packages.shared.queue import (
    JOB_PRIORITIES,
    GetJobsResult,
    IFQueueStorageAdapter,
    IJob,
    JobPriority,
    QueueKey,
    QueueStatus,
)




class IJobs(TypedDict):
    priority_0: dict[str, IJob]
    priority_1: dict[str, IJob]
    priority_2: dict[str, IJob]
    priority_3: dict[str, IJob]
    priority_4: dict[str, IJob]
    priority_5: dict[str, IJob]
    priority_6: dict[str, IJob]
    priority_7: dict[str, IJob]
    priority_8: dict[str, IJob]
    priority_9: dict[str, IJob]


class IQueues(TypedDict):
    jobs: IJobs


class QueueStorageJSONAdapter(IFQueueStorageAdapter):
    def __init__(self) -> None:
        if os.path.exists("./queue.json"):
            with open("./queue.json", mode="r", encoding="utf-8") as f:
                queues: IQueues = json.load(f)
        else:
            queues: IQueues = {
                "jobs": {
                    "priority_0": {},
                    "priority_1": {},
                    "priority_2": {},
                    "priority_3": {},
                    "priority_4": {},
                    "priority_5": {},
                    "priority_6": {},
                    "priority_7": {},
                    "priority_8": {},
                    "priority_9": {},
                }
            }
        self.queues = queues

    async def save_file(self):
        with open("./queue.json", mode="w", encoding="utf-8") as f:
            json.dump(self.queues, f, ensure_ascii=False, indent=4)

    async def add_job(self, key: QueueKey, *args, **kwargs):
        self.queues["jobs"][f"priority_{key.priority}"][key.identifier] = {
            "identifier": key.code,
            "priority": key.priority,
            "name": key.name,
            "status": key.status,
            "args": args,
            "kwargs": kwargs,
        }
        await self.save_file()

    async def get_jobs(
        self, name: str, limit: int, status: QueueStatus
    ) -> list[GetJobsResult]:
        result: list[GetJobsResult] = []
        for priority in JOB_PRIORITIES:
            if len(result) == limit:
                break
            for key, job in self.queues["jobs"][f"priority_{priority}"].items():
                _status = job["status"]
                _name = job["name"]
                if priority == priority and status == _status and name == _name:
                    _args = job["args"]
                    _kwargs = job["kwargs"]
                    _status = job["status"]
                    result.append(GetJobsResult(key=key, args=_args, kwargs=_kwargs, identifier=key, status=_status, priority=priority))  # type: ignore
                    if len(result) == limit:
                        break
                continue
        return result

    async def remove_by_key(self, key_id: str, priority: int):
        del self.queues["jobs"][f"priority_{priority}"][key_id]
        await self.save_file()

    async def complete_job(self, name: str, key: QueueKey):
        completed_number = await self.count_jobs(name, "completed")
        if completed_number > 50:
            completed_jobs = await self.get_jobs(name, 20, "completed")
            for job in completed_jobs:
                await self.remove_by_key(job["identifier"], priority=job["priority"])

    async def count_jobs(self, name: str, status: QueueStatus) -> int:
        count = 0
        for priority in JOB_PRIORITIES:
            for job in self.queues["jobs"][f"priority_{priority}"].values():
                if job["status"] == status and job["name"] == name:
                    count = count + 1
        return count

    async def update_status(
        self,
        key: QueueKey,
        name: str,
        status: QueueStatus,
        priority: JobPriority | None = None,
    ):
        new_priority = priority or key.priority
        new_key = await key.update(status=status, priority=new_priority)
        self.queues["jobs"][f"priority_{key.priority}"][key.identifier][
            "status"
        ] = status
        await self.save_file()

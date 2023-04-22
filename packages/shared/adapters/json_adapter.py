import json
import os
from packages.shared.queue import JOB_PRIORITIES, GetJobsResult, IFQueueStorageAdapter, JobPriority, QueueStatus, generate_queue_key

class QueueStorageJSONAdapter(IFQueueStorageAdapter):
    def __init__(self) -> None:
        if os.path.exists('./queue.json'):
            with open('./queue.json', mode='r', encoding='utf-8') as f:
                queues = json.load(f)
        else:
            queues = {}
        self.queues = queues

    async def save_file(self):
        with open('./queue.json', mode='w', encoding='utf-8') as f:
            json.dump(self.queues, f, ensure_ascii=False)
    
    async def add_job(self, key: str, *args, **kwargs):
        self.queues[key] = {'args': args, 'kwargs': kwargs}
        await self.save_file()

    async def get_jobs(self, name: str, limit: int, status: QueueStatus) -> list[GetJobsResult]:
        result: list[GetJobsResult] = []
        for priority in JOB_PRIORITIES:
            if len(result) == limit:
                break
            for key in self.queues.keys():
                if key.startswith(f'{priority}:{status}:{name}:'):
                    value = self.queues[key]
                    result.append(GetJobsResult(key=key, args=value['args'], kwargs=value['kwargs']))
                    if len(result) == limit:
                        break
        return result

    async def remove_by_key(self, key: str):
        del self.queues[key]
        await self.save_file()

    async def complete_job(self, name:str, key: str):
        completed_number = await self.count_jobs(name, 'completed')
        if completed_number > 50:
            completed_jobs = await self.get_jobs(name, 20, 'completed')
            for job in completed_jobs:
                await self.remove_by_key(job['key'])
        
        # await redis_connection.delete(key)

    async def count_jobs(self, name: str, status: QueueStatus) -> int:
        count = 0
        for key in self.queues.keys():
            if key.find(f'{status}:{name}:') != -1:
                count = count + 1
        return count

    async def update_status(self, key:str, name: str, status: QueueStatus, priority: JobPriority|None=None) -> str:
        original_priority = int(key.split(':')[0])
        new_priority =  priority if priority else original_priority
        new_key = generate_queue_key(name, status, priority=new_priority)
        data = self.queues.pop(key)        
        if data is None:
            raise Exception('指定されたジョブは存在しません')
        self.queues[new_key] = data
        await self.save_file()
        return new_key
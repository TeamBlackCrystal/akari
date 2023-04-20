from abc import ABC, abstractmethod
import asyncio
import uuid
from typing import Any, Callable, Generic, Literal, TypeVar, TypedDict

QueueStatus = Literal['waiting', 'running', 'completed']
JobPriority = Literal[0, 1, 2, 3, 4,5,6,7,8,9]
JOB_PRIORITIES: list[int] = [0, 1, 2, 3, 4,5,6,7,8,9]

def generate_queue_key(name: str, status: QueueStatus = 'waiting', priority: int=9):
    return f'{priority}:{status}:{name}:{uuid.uuid4()}'

class GetJobsResult(TypedDict):
    key: str
    kwargs: dict[str, Any]
    args: tuple[Any, ...]


class IFQueueStorageAdapter(ABC):
    @abstractmethod
    async def add_job(self, key: str, priority: JobPriority=9, *args, **kwargs):
        ...

    @abstractmethod
    async def get_jobs(
        self, name: str, limit: int, status: QueueStatus
    ) -> list[GetJobsResult]:
        ...

    @abstractmethod
    async def complete_job(self, name: str):
        ...
        
    @abstractmethod
    async def update_status(self, key:str, name:str, status: QueueStatus, priority: JobPriority|None=None)  -> str:
        """ジョブのステータスを更新します

        Parameters
        ----------
        key : str
            元のキー
        name : str
            ジョブキューの名前
        status : QueueStatus
            新しいステータス

        Returns
        -------
        str
            新しいキー
        """
        ...

    @abstractmethod
    async def count_jobs(self, name: str, status: QueueStatus) -> int:
        """指定された状態のジョブの総数を返します

        Parameters
        ----------
        name : str
            キューの名前
        status : QueueStatus
            ジョブの状態

        Returns
        -------
        int
            ジョブの総数
        """
        ...


class QueueSystem:
    def __init__(
        self,
        name: str,
        func: Callable | None=None,
        success_func: Callable | None=None,
        max_process: int = 5,
        cooldown: int = 5,
        *,
        queue_storage_adapter: IFQueueStorageAdapter,
    ) -> None:
        self.is_startup:bool = True
        self.name = name
        self.func = func
        self.success_func = success_func
        self.max_process: int = max_process
        self.current_run_process_number: int = 0
        self.cooldown = cooldown
        self.next_stop = False
        self.queue_storage_adapter: IFQueueStorageAdapter = queue_storage_adapter
        self.loop = asyncio.get_event_loop()

    def run(self) -> asyncio.Task[None]:
        if self.func is None or self.success_func is None:
            raise Exception('func 又は success_funcが定義されていません')
        task = self.loop.create_task(self.scheduler())
        return task

    def stop(self) -> None:
        self.next_stop = True



    async def count_jobs(self, status: QueueStatus='waiting'):
        return await self.queue_storage_adapter.count_jobs(name=self.name, status=status)

    async def add(self, priority: JobPriority=9, *args, **kwargs):
        # キーは 状態:キューの名前:uuid で構成される
        await self.queue_storage_adapter.add_job(
            generate_queue_key(self.name, status='waiting', priority=priority), *args, **kwargs
        )

    async def get_queues(self, status: QueueStatus):
        return await self.queue_storage_adapter.get_jobs(
            name=self.name,
            limit=self.max_process - self.current_run_process_number,
            status=status,
        )

    async def scheduler(self):
        while True:
            if self.next_stop:
                return
            if self.current_run_process_number < self.max_process:
                if self.is_startup:
                    jobs = await self.get_queues('running')
                    self.is_startup = False
                else:
                    jobs = await self.get_queues('waiting')
                for job in jobs:
                    if (
                        self.current_run_process_number < self.max_process
                    ):  # 現在実行中のプロセスが最大プロセス以下か確認
                        # 処理開始
                        self.current_run_process_number = (
                            self.current_run_process_number + 1
                        )

                        self.loop.create_task(
                            self.task(job['key'], *job['args'], **job['kwargs'])
                        )

            await asyncio.sleep(self.cooldown)

    async def task(self, key, *args, **kwargs):
        if self.func is None or self.success_func is None:
            raise Exception('func 又は success_funcが定義されていません')
        running_key = await self.queue_storage_adapter.update_status(key, self.name, 'running')
        await self.func(*args, **kwargs)
        new_key = await self.queue_storage_adapter.update_status(running_key, self.name, 'completed')

        await self.success_func(new_key, *args, **kwargs)
        # 処理終了後
        await self.queue_storage_adapter.complete_job(new_key)
        self.current_run_process_number = self.current_run_process_number - 1
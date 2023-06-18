from abc import ABC, abstractmethod
import asyncio
import uuid
from typing import Any, Callable, Literal, TypedDict


QueueStatus = Literal["waiting", "running", "completed", "failed"]
JobPriority = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
JOB_PRIORITIES: list[int] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


class IJob(TypedDict):
    identifier: str
    priority: JobPriority
    name: str
    status: QueueStatus
    args: tuple[Any]
    kwargs: dict[str, Any]






class QueueKey:
    def __init__(
        self,
        name: str,
        status: QueueStatus = "waiting",
        priority: int = 9,
        identifier: str | None = None,
    ) -> None:
        self.priority = priority
        self.status = status
        self.name = name
        self.identifier = identifier if identifier else str(uuid.uuid4())

    async def update(self, status: QueueStatus, priority: int = 9):
        self.status = status
        self.priority = priority

    @property
    def code(self):
        return f"{self.priority}:{self.status}:{self.name}:{self.identifier}"


class GetJobsResult(TypedDict):
    identifier: str
    key: str
    priority: JobPriority
    status: QueueStatus
    kwargs: dict[str, Any]
    args: tuple[Any, ...]


class IFQueueStorageAdapter(ABC):
    @abstractmethod
    async def add_job(self, key: QueueKey, priority: JobPriority = 9, *args, **kwargs):
        ...

    @abstractmethod
    async def get_jobs(
        self, name: str, limit: int, status: QueueStatus
    ) -> list[GetJobsResult]:
        ...

    @abstractmethod
    async def complete_job(self, name: str, key: QueueKey):
        ...

    @abstractmethod
    async def update_status(
        self,
        key: QueueKey,
        name: str,
        status: QueueStatus,
        priority: JobPriority | None = None,
    ):
        """ジョブのステータスを更新します

        Parameters
        ----------
        key : QueueKey
            キー
        name : str
            ジョブキューの名前
        status : QueueStatus
            新しいステータス
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
        func: Callable | None = None,
        success_func: Callable | None = None,
        max_process: int = 5,
        max_retry: int = 5,
        cooldown: int = 5,
        *,
        queue_storage_adapter: IFQueueStorageAdapter,
    ) -> None:
        self.is_startup: bool = True
        self.name = name
        self.func = func
        self.success_func = success_func
        self.max_process: int = max_process
        self.current_run_process_number: int = 0
        self.max_retry = max_retry
        self.cooldown = cooldown
        self.next_stop = False
        self.queue_storage_adapter: IFQueueStorageAdapter = queue_storage_adapter
        self.loop = asyncio.get_event_loop()

    def run(self) -> asyncio.Task[None]:
        if self.func is None:
            raise Exception("funcが定義されていません")
        task = self.loop.create_task(self.scheduler())
        return task

    def stop(self) -> None:
        self.next_stop = True

    async def count_jobs(self, status: QueueStatus = "waiting"):
        return await self.queue_storage_adapter.count_jobs(
            name=self.name, status=status
        )

    async def add(self, priority: JobPriority = 9, *args, **kwargs):
        # キーは 状態:キューの名前:uuid で構成される
        await self.queue_storage_adapter.add_job(
            QueueKey(self.name, status="waiting", priority=priority),
            *args,
            **kwargs,
        )

    async def get_queues(self, status: QueueStatus):
        return await self.queue_storage_adapter.get_jobs(
            name=self.name,
            limit=self.max_process - self.current_run_process_number,
            status=status,
        )

    async def count_running_process(self):
        return await self.count_jobs(status="running")

    async def scheduler(self):
        while True:
            if self.next_stop:
                return

            running_process_number = await self.count_running_process()
            if running_process_number <= self.max_process or self.is_startup:
                allow_add_job_number = self.max_process - running_process_number
                if self.is_startup:
                    jobs = await self.get_queues("running")
                    if len(jobs) == 0:
                        jobs = await self.get_queues("waiting")
                        self.is_startup = False
                else:
                    jobs = await self.get_queues("waiting")
                count = 1
                for job in jobs:
                    if (
                        count <= allow_add_job_number or self.is_startup
                    ):  # 現在実行中のプロセスが最大プロセス以下か確認
                        if self.is_startup and running_process_number == 0:
                            self.is_startup = False
                        print('実行開始:', job)
                        self.loop.create_task(
                            self.task(
                                QueueKey(
                                    name=self.name,
                                    status=job["status"],
                                    priority=job["priority"],
                                    identifier=job["identifier"],
                                ),
                                *job["args"],
                                **job["kwargs"],
                            ),
                            name=f'queue: {job["key"]}',
                        )
                        count = count + 1
                    # continue

            await asyncio.sleep(self.cooldown)

    async def task(self, key: QueueKey, *args, **kwargs):
        if self.func is None:
            raise Exception("funcが定義されていません")
        await self.queue_storage_adapter.update_status(key, self.name, "running")
        try:
            await self.func(*args, **kwargs)
        except Exception as e:
            await self.queue_storage_adapter.update_status(key, self.name, "failed")
            return

        await self.queue_storage_adapter.update_status(key, self.name, "completed")
        if self.success_func:
            await self.success_func(self.name, key, *args, **kwargs)
        # 処理終了後
        await self.queue_storage_adapter.complete_job(self.name, key)
        self.current_run_process_number = self.current_run_process_number - 1
        return

from injector import Binder, Module
from packages.shared.adapters.json_adapter import QueueStorageJSONAdapter
from packages.shared.adapters.redis import RedisQueueSystem

from packages.shared.queue import IFQueueStorageAdapter
from packages.shared.config import config

class QueueModule(Module):
    def configure(self, binder: Binder) -> None:
        print(config.job_queue.type == 'redis', config.job_queue.type)
        binder.bind(IFQueueStorageAdapter, RedisQueueSystem if config.job_queue.type == 'redis' else QueueStorageJSONAdapter)

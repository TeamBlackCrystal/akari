from packages.shared.adapters.redis import RedisQueueSystem
from packages.shared.queue import QueueSystem

readonly_notfound_fixer_queue = QueueSystem('notfound_fixer', queue_storage_adapter=RedisQueueSystem())

import redis.asyncio as redis
from mipac.utils.format import remove_dict_empty

from packages.shared.config import config


def get_redis():
    arg = remove_dict_empty({'db': config.redis.db, 'password': config.redis.password})
    return redis.Redis(host=config.redis.host, port=config.redis.port, **arg)
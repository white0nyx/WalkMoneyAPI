import redis.asyncio as redis

from src.common.configuration import conf

redis_client = redis.Redis(host=conf.redis.host, port=conf.redis.port, db=conf.redis.db, password=conf.redis.passwd, decode_responses=True)

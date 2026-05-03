from redis.asyncio import Redis
import json


class RedisCache:
    def __init__(self, redis: Redis):
        self.redis = redis
        
    async def get(self, key:str) -> dict | None:
        result = await self.redis.get(key)
        if result is not None:
            return self._deserialize(result)
        return None
    
    async def set(self, key: str, value: dict, ttl: int | None = None  ) -> None:
        value = self._serialize(value)
        await self.redis.set(key, value, ex=ttl)
        
    def _serialize(self, value):
        return json.dumps(value)

    def _deserialize(self, value):
        return json.loads(value)
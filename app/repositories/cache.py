from redis.asyncio import Redis


class CacheRepository:
    def __init__(
        self,
        redis: Redis,
    ):
        self.redis = redis

    async def get(
        self,
        key: str,
    ) -> str | None:
        return await self.redis.get(key)

    async def set(
        self,
        key: str,
        value: str,
        expire: int | None = None,
    ) -> None:
        await self.redis.set(
            key,
            value,
            ex=expire,
        )

    async def delete(
        self,
        key: str,
    ) -> None:
        await self.redis.delete(key)

    async def exists(
        self,
        key: str,
    ) -> bool:
        return bool(
            await self.redis.exists(key)
        )
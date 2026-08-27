import json

from fastapi import HTTPException
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CV, utc_now

from app.repositories import (
    CacheRepository,
    CVRepository,
)

from app.schemas import (
    CVCreate,
    CVUpdate,
)


class CVService:
    CACHE_TTL = 300

    def __init__(
        self,
        session: AsyncSession,
        redis: Redis,
    ):
        self.session = session
        self.repository = CVRepository(
            session
        )
        self.cache = CacheRepository(
            redis
        )

    def _cache_key(
        self,
        cv_id: int,
    ) -> str:
        return f"cv:{cv_id}"

    def _user_cache_key(
        self,
        user_id: int,
    ) -> str:
        return f"user:{user_id}:cvs"

    async def create(
        self,
        user_id: int,
        data: CVCreate,
    ) -> CV:
        cv = CV(
            user_id=user_id,
            title=data.title,
        )

        await self.repository.create(
            cv
        )

        await self.session.commit()
        await self.session.refresh(
            cv
        )

        await self.cache.delete(
            self._user_cache_key(user_id)
        )

        return cv

    async def get_by_id(
        self,
        cv_id: int,
        user_id: int,
    ) -> CV:
        cache_key = self._cache_key(
            cv_id
        )

        cached = await self.cache.get(
            cache_key
        )

        if cached is not None:
            data = json.loads(
                cached
            )

            if data["user_id"] != user_id:
                raise HTTPException(
                    status_code=404,
                    detail="CV not found",
                )

            return CV.model_validate(
                data
            )

        cv = await self.repository.get_by_id(
            cv_id
        )

        if (
            cv is None
            or cv.user_id != user_id
        ):
            raise HTTPException(
                status_code=404,
                detail="CV not found",
            )

        await self.cache.set(
            cache_key,
            json.dumps(
                cv.model_dump(
                    mode="json"
                )
            ),
            expire=self.CACHE_TTL,
        )

        return cv

    async def get_by_user_id(
        self,
        user_id: int,
    ) -> list[CV]:
        cache_key = self._user_cache_key(
            user_id
        )

        cached = await self.cache.get(
            cache_key
        )

        if cached is not None:
            return [
                CV.model_validate(
                    item
                )
                for item in json.loads(
                    cached
                )
            ]

        cvs = await self.repository.get_by_user_id(
            user_id
        )

        await self.cache.set(
            cache_key,
            json.dumps(
                [
                    cv.model_dump(
                        mode="json"
                    )
                    for cv in cvs
                ]
            ),
            expire=self.CACHE_TTL,
        )

        return cvs

    async def update(
        self,
        cv_id: int,
        user_id: int,
        data: CVUpdate,
    ) -> CV:
        cv = await self.get_by_id(
            cv_id,
            user_id,
        )

        values = data.model_dump(
            exclude_unset=True
        )

        for field, value in values.items():
            setattr(
                cv,
                field,
                value,
            )

        cv.updated_at = utc_now()

        await self.repository.update(
            cv
        )

        await self.session.commit()
        await self.session.refresh(
            cv
        )

        await self.cache.delete(
            self._cache_key(cv_id)
        )

        await self.cache.delete(
            self._user_cache_key(user_id)
        )

        return cv

    async def delete(
        self,
        cv_id: int,
        user_id: int,
    ) -> None:
        cv = await self.get_by_id(
            cv_id,
            user_id,
        )

        await self.repository.delete(
            cv
        )

        await self.session.commit()

        await self.cache.delete(
            self._cache_key(cv_id)
        )

        await self.cache.delete(
            self._user_cache_key(user_id)
        )
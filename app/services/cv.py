import json
from math import ceil

from fastapi import HTTPException
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CV, utc_now

from app.repositories import (
    CacheRepository,
    CVCertificationRepository,
    CVEducationRepository,
    CVExperienceRepository,
    CVLanguageRepository,
    CVPersonalInfoRepository,
    CVProjectRepository,
    CVRepository,
    CVSkillRepository,
)

from app.schemas import (
    CVCertificationRead,
    CVCreate,
    CVDetailRead,
    CVEducationRead,
    CVExperienceRead,
    CVLanguageDetailRead,
    CVPageRead,
    CVPersonalInfoRead,
    CVProjectRead,
    CVRead,
    CVSkillDetailRead,
    CVUpdate,
)


class CVService:
    CACHE_TTL = 300
    MAX_PAGE_SIZE = 100

    def __init__(
        self,
        session: AsyncSession,
        redis: Redis,
    ):
        self.session = session

        self.repository = CVRepository(
            session
        )

        self.personal_info_repository = (
            CVPersonalInfoRepository(
                session
            )
        )

        self.experience_repository = (
            CVExperienceRepository(
                session
            )
        )

        self.education_repository = (
            CVEducationRepository(
                session
            )
        )

        self.skill_repository = (
            CVSkillRepository(
                session
            )
        )

        self.project_repository = (
            CVProjectRepository(
                session
            )
        )

        self.language_repository = (
            CVLanguageRepository(
                session
            )
        )

        self.certification_repository = (
            CVCertificationRepository(
                session
            )
        )

        self.cache = CacheRepository(
            redis
        )

    # ==========================================
    # Cache Keys
    # ==========================================

    def _detail_cache_key(
        self,
        cv_id: int,
    ) -> str:
        return f"cv:{cv_id}:detail"

    def _search_cache_key(
        self,
        user_id: int,
        query: str | None,
        page: int,
        page_size: int,
    ) -> str:
        normalized_query = (
            query.strip().lower()
            if query
            else "all"
        )

        return (
            f"user:{user_id}:cvs:"
            f"{normalized_query}:"
            f"{page}:"
            f"{page_size}"
        )

    def _user_cache_pattern(
        self,
        user_id: int,
    ) -> str:
        return f"user:{user_id}:cvs:*"

    # ==========================================
    # Cache Invalidation
    # ==========================================

    async def _invalidate_user_cache(
        self,
        user_id: int,
    ) -> None:
        pattern = self._user_cache_pattern(
            user_id
        )

        await self.cache.delete_pattern(
            pattern
        )

    async def _invalidate_cv_cache(
        self,
        cv_id: int,
        user_id: int,
    ) -> None:
        await self.cache.delete(
            self._detail_cache_key(
                cv_id
            )
        )

        await self._invalidate_user_cache(
            user_id
        )

    # ==========================================
    # Build Detail Response
    # ==========================================

    async def _build_detail_response(
        self,
        cv: CV,
    ) -> CVDetailRead:
        cv_id = cv.id

        if cv_id is None:
            raise HTTPException(
                status_code=500,
                detail="Invalid CV identifier",
            )

        personal_info = (
            await self.personal_info_repository.get_by_cv_id(
                cv_id
            )
        )

        experience = (
            await self.experience_repository.get_by_cv_id(
                cv_id
            )
        )

        education = (
            await self.education_repository.get_by_cv_id(
                cv_id
            )
        )

        skills_data = (
            await self.skill_repository.get_with_skills(
                cv_id
            )
        )

        projects = (
            await self.project_repository.get_by_cv_id(
                cv_id
            )
        )

        languages_data = (
            await self.language_repository.get_with_languages(
                cv_id
            )
        )

        certifications = (
            await self.certification_repository.get_by_cv_id(
                cv_id
            )
        )

        return CVDetailRead(
            id=cv.id,
            user_id=cv.user_id,
            title=cv.title,
            created_at=cv.created_at,
            updated_at=cv.updated_at,

            personal_info=(
                CVPersonalInfoRead.model_validate(
                    personal_info
                )
                if personal_info is not None
                else None
            ),

            experience=[
                CVExperienceRead.model_validate(
                    item
                )
                for item in experience
            ],

            education=[
                CVEducationRead.model_validate(
                    item
                )
                for item in education
            ],

            skills=[
                CVSkillDetailRead(
                    id=skill.id,
                    name=skill.name,
                    level=cv_skill.level,
                    sort_order=cv_skill.sort_order,
                )
                for cv_skill, skill in skills_data
            ],

            projects=[
                CVProjectRead.model_validate(
                    item
                )
                for item in projects
            ],

            languages=[
                CVLanguageDetailRead(
                    id=language.id,
                    name=language.name,
                    proficiency=cv_language.proficiency,
                    sort_order=cv_language.sort_order,
                )
                for cv_language, language in languages_data
            ],

            certifications=[
                CVCertificationRead.model_validate(
                    item
                )
                for item in certifications
            ],
        )

    # ==========================================
    # Create
    # ==========================================

    async def create(
        self,
        user_id: int,
        data: CVCreate,
    ) -> CVRead:
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

        await self._invalidate_user_cache(
            user_id
        )

        return CVRead.model_validate(
            cv
        )

    # ==========================================
    # Get Detail
    # ==========================================

    async def get_by_id(
        self,
        cv_id: int,
        user_id: int,
    ) -> CVDetailRead:
        cache_key = self._detail_cache_key(
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

            return CVDetailRead.model_validate(
                data
            )

        cv = await self.repository.get_by_id_for_user(
            cv_id=cv_id,
            user_id=user_id,
        )

        if cv is None:
            raise HTTPException(
                status_code=404,
                detail="CV not found",
            )

        detail = await self._build_detail_response(
            cv
        )

        await self.cache.set(
            cache_key,
            json.dumps(
                detail.model_dump(
                    mode="json"
                )
            ),
            expire=self.CACHE_TTL,
        )

        return detail

    # ==========================================
    # Search With Pagination
    # ==========================================

    async def search(
        self,
        user_id: int,
        query: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> CVPageRead:
        if page < 1:
            page = 1

        if page_size < 1:
            page_size = 10

        if page_size > self.MAX_PAGE_SIZE:
            page_size = self.MAX_PAGE_SIZE

        if query is not None:
            query = query.strip()

            if not query:
                query = None

        cache_key = self._search_cache_key(
            user_id=user_id,
            query=query,
            page=page,
            page_size=page_size,
        )

        cached = await self.cache.get(
            cache_key
        )

        if cached is not None:
            return CVPageRead.model_validate(
                json.loads(
                    cached
                )
            )

        offset = (
            page - 1
        ) * page_size

        cvs, total = (
            await self.repository.search_by_user(
                user_id=user_id,
                query=query,
                offset=offset,
                limit=page_size,
            )
        )

        pages = (
            ceil(total / page_size)
            if total > 0
            else 0
        )

        response = CVPageRead(
            items=[
                CVRead.model_validate(
                    cv
                )
                for cv in cvs
            ],
            total=total,
            page=page,
            page_size=page_size,
            pages=pages,
        )

        await self.cache.set(
            cache_key,
            json.dumps(
                response.model_dump(
                    mode="json"
                )
            ),
            expire=self.CACHE_TTL,
        )

        return response

    # ==========================================
    # Update
    # ==========================================

    async def update(
        self,
        cv_id: int,
        user_id: int,
        data: CVUpdate,
    ) -> CVRead:
        cv = await self.repository.get_by_id_for_user(
            cv_id=cv_id,
            user_id=user_id,
        )

        if cv is None:
            raise HTTPException(
                status_code=404,
                detail="CV not found",
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

        await self._invalidate_cv_cache(
            cv_id=cv_id,
            user_id=user_id,
        )

        return CVRead.model_validate(
            cv
        )

    # ==========================================
    # Delete
    # ==========================================

    async def delete(
        self,
        cv_id: int,
        user_id: int,
    ) -> None:
        cv = await self.repository.get_by_id_for_user(
            cv_id=cv_id,
            user_id=user_id,
        )

        if cv is None:
            raise HTTPException(
                status_code=404,
                detail="CV not found",
            )

        await self.repository.delete(
            cv
        )

        await self.session.commit()

        await self._invalidate_cv_cache(
            cv_id=cv_id,
            user_id=user_id,
        )
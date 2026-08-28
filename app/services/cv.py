# Standard library imports used for JSON serialization and pagination.
import json
from math import ceil

from fastapi import HTTPException
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.models.cv import CV, utc_now

# Repositories used to access PostgreSQL and Redis.
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
    UserRepository,
)

# Schemas used for request validation and API responses.
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
    """Handle business logic for CV operations."""

    # Cache entries expire after five minutes.
    CACHE_TTL = 300

    # Limit the maximum number of items returned in one page.
    MAX_PAGE_SIZE = 100

    def __init__(
        self,
        session: AsyncSession,
        redis: Redis,
    ):
        """Initialize the service dependencies."""
        self.session = session

        self.repository = CVRepository(
            session
        )

        self.user_repository = UserRepository(
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

    def _detail_cache_key(
        self,
        cv_id: int,
    ) -> str:
        """Build the cache key for a CV detail."""
        return f"cv:{cv_id}:detail"

    def _search_cache_key(
        self,
        user_id: int,
        query: str | None,
        page: int,
        page_size: int,
    ) -> str:
        """Build the cache key for a user's CV list."""
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
        """Build a pattern for all cached CV lists of a user."""
        return f"user:{user_id}:cvs:*"

    async def _invalidate_user_cache(
        self,
        user_id: int,
    ) -> None:
        """Remove all cached CV lists for a user."""
        await self.cache.delete_pattern(
            self._user_cache_pattern(
                user_id
            )
        )

    async def _invalidate_cv_cache(
        self,
        cv_id: int,
        user_id: int,
    ) -> None:
        """Remove cached data affected by a CV change."""
        await self.cache.delete(
            self._detail_cache_key(
                cv_id
            )
        )

        # The user's cached CV lists are also affected.
        await self._invalidate_user_cache(
            user_id
        )

    async def _ensure_user(
        self,
        user_id: int,
    ) -> User:
        """Ensure that a local user reference exists."""
        user = await self.user_repository.get_by_id(
            user_id
        )

        if user is None:
            # The ID comes from the authenticated user's JWT.
            user = User(
                id=user_id
            )

            await self.user_repository.create(
                user
            )

        return user

    async def _build_detail_response(
        self,
        cv: CV,
    ) -> CVDetailRead:
        """Build a detailed CV response from its related data."""
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

    async def create(
        self,
        user_id: int,
        data: CVCreate,
    ) -> CVRead:
        """Create a new CV for a user."""
        await self._ensure_user(
            user_id
        )

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

        # Creating a CV invalidates the cached CV lists.
        await self._invalidate_user_cache(
            user_id
        )

        return CVRead.model_validate(
            cv
        )

    async def get_by_id(
        self,
        cv_id: int,
        user_id: int,
    ) -> CVDetailRead:
        """Return a CV with all related data."""
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

            # The detail cache is shared by CV ID, so ownership must still
            # be checked before returning the cached response.
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

    async def search(
        self,
        user_id: int,
        query: str | None = None,
        page: int = 1,
        page_size: int = 10,
    ) -> CVPageRead:
        """Return a paginated list of a user's CVs."""
        if page < 1:
            page = 1

        if page_size < 1:
            page_size = 10

        if page_size > self.MAX_PAGE_SIZE:
            page_size = self.MAX_PAGE_SIZE

        # Normalize the query so equivalent searches use the same cache key.
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

    async def update(
        self,
        cv_id: int,
        user_id: int,
        data: CVUpdate,
    ) -> CVRead:
        """Update a user's CV."""
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

    async def delete(
        self,
        cv_id: int,
        user_id: int,
    ) -> None:
        """Delete a user's CV."""
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
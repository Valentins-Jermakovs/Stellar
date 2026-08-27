from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas import CVTemplate
from app.services import (
    CVDocumentService,
    CVGeneratorService,
)


class CVGeneratorFacade:
    def __init__(
        self,
        session: AsyncSession,
        templates_path: Path,
    ):
        self.document_service = CVDocumentService(
            session
        )

        self.generator_service = CVGeneratorService(
            templates_path
        )

    async def generate(
        self,
        cv_id: int,
        user_id: int,
        template: CVTemplate,
    ) -> bytes:
        document = (
            await self.document_service.get_document(
                cv_id=cv_id,
                user_id=user_id,
            )
        )

        return self.generator_service.generate(
            document=document,
            template=template,
        )
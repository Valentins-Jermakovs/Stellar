# ==============================
# Library imports
# ==============================

from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession


# ==============================
# Application imports
# ==============================

from app.schemas import (
    CVLocale,
    CVTemplate,
)

from app.services import (
    CVDocumentService,
    CVGeneratorService,
)


# ==============================
# CV generator facade
# ==============================

class CVGeneratorFacade:
    """
    Provide a simplified interface for CV generation.
    """

    def __init__(
        self,
        session: AsyncSession,
        templates_path: Path,
    ):
        """
        Initialize document and generator services.
        """

        self.document_service = CVDocumentService(
            session
        )

        self.generator_service = CVGeneratorService(
            templates_path=templates_path,
        )

    async def generate(
        self,
        cv_id: int,
        user_id: int,
        template: CVTemplate,
        language: CVLocale,
    ) -> bytes:
        """
        Generate a CV PDF using the selected template and language.
        """

        document = await self.document_service.get_document(
            cv_id=cv_id,
            user_id=user_id,
            template=template,
        )

        return self.generator_service.generate(
            document=document,
            template=template,
            language=language,
        )
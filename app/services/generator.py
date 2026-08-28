from pathlib import Path

from jinja2 import (
    Environment,
    FileSystemLoader,
    TemplateNotFound,
)
from weasyprint import HTML

from app.schemas import (
    CVDocument,
    CVLocale,
    CVTemplate,
)
from app.utils import (
    TRANSLATIONS,
    format_month_year,
    format_year,
)


class CVGeneratorService:
    """Generate PDF documents from CV templates."""

    def __init__(
        self,
        templates_path: Path,
    ):
        """Initialize the Jinja template environment."""
        self.templates_path = templates_path

        self.environment = Environment(
            loader=FileSystemLoader(
                templates_path
            ),
            autoescape=True,
        )

        self.environment.filters[
            "month_year"
        ] = format_month_year

        self.environment.filters[
            "year"
        ] = format_year

    def _get_template_path(
        self,
        template: CVTemplate,
    ) -> str:
        """Build the template path for the selected CV template."""
        return (
            f"{template.value}/template.html"
        )

    def generate(
        self,
        document: CVDocument,
        template: CVTemplate,
        language: CVLocale,
    ) -> bytes:
        """Generate a PDF using the selected template and language."""
        template_path = self._get_template_path(
            template
        )

        try:
            template_file = self.environment.get_template(
                template_path
            )
        except TemplateNotFound as exc:
            raise ValueError(
                f"Template not found: {template.value}"
            ) from exc

        translations = TRANSLATIONS.get(
            language.value
        )

        if translations is None:
            raise ValueError(
                f"Translations not found: {language.value}"
            )

        html = template_file.render(
            cv=document,
            language=language.value,
            translations=translations,
        )

        return HTML(
            string=html,
            base_url=str(
                self.templates_path
                / template.value
            ),
        ).write_pdf()
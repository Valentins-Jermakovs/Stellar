# ==============================
# Library imports
# ==============================

from pathlib import Path

from jinja2 import (
    Environment,
    FileSystemLoader,
    TemplateNotFound,
)

from weasyprint import HTML


# ==============================
# Application imports
# ==============================

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


# ==============================
# CV generator service
# ==============================

class CVGeneratorService:
    """
    This service generates PDF documents from CV templates.

    It uses Jinja2 to render HTML templates and WeasyPrint
    to convert the rendered HTML into a PDF document.
    """

    def __init__(
        self,
        templates_path: Path,
    ):
        """
        Initialize the CV generator service.

        The Jinja2 environment is configured with the directory
        containing the CV templates and custom date formatting filters.
        """

        # Path to the directory containing CV templates.
        self.templates_path = templates_path

        # Configure the Jinja2 template environment.
        self.environment = Environment(
            loader=FileSystemLoader(
                templates_path
            ),
            autoescape=True,
        )

        # Register the month and year formatting filter.
        self.environment.filters[
            "month_year"
        ] = format_month_year

        # Register the year formatting filter.
        self.environment.filters[
            "year"
        ] = format_year

    # Build the path to the selected CV template.
    def _get_template_path(
        self,
        template: CVTemplate,
    ) -> str:
        """
        Build the template path for the selected CV template.
        """

        return (
            f"{template.value}/template.html"
        )

    # Generate a PDF document from a CV.
    def generate(
        self,
        document: CVDocument,
        template: CVTemplate,
        language: CVLocale,
    ) -> bytes:
        """
        Generate a PDF using the selected template and language.

        The CV document is rendered using the corresponding Jinja2
        template and translated according to the selected locale.
        The resulting HTML is then converted into a PDF document.
        """

        # Build the path to the selected template.
        template_path = self._get_template_path(
            template
        )

        # Load the selected Jinja2 template.
        try:
            template_file = self.environment.get_template(
                template_path
            )
        except TemplateNotFound as exc:
            raise ValueError(
                f"Template not found: {template.value}"
            ) from exc

        # Retrieve translations for the selected language.
        translations = TRANSLATIONS.get(
            language.value
        )

        if translations is None:
            raise ValueError(
                f"Translations not found: {language.value}"
            )

        # Render the HTML template with the CV data.
        html = template_file.render(
            cv=document,
            language=language.value,
            translations=translations,
        )

        # Convert the rendered HTML into a PDF document.
        return HTML(
            string=html,
            base_url=str(
                self.templates_path
                / template.value
            ),
        ).write_pdf()
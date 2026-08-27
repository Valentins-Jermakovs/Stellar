from pathlib import Path

from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from weasyprint import HTML

from app.schemas import CVDocument, CVTemplate


class CVGeneratorService:
    def __init__(
        self,
        templates_path: Path,
    ):
        self.templates_path = templates_path

        self.environment = Environment(
            loader=FileSystemLoader(
                templates_path
            ),
            autoescape=True,
        )

    def _get_template_path(
        self,
        template: CVTemplate,
    ) -> str:
        return (
            f"{template.value}/template.html"
        )

    def generate(
        self,
        document: CVDocument,
        template: CVTemplate,
    ) -> bytes:
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

        html = template_file.render(
            cv=document
        )

        return HTML(
            string=html,
            base_url=str(
                self.templates_path
                / template.value
            ),
        ).write_pdf()
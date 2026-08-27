from pathlib import Path

from jinja2 import Environment, FileSystemLoader
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

    def generate(
        self,
        document: CVDocument,
        template: CVTemplate,
    ) -> bytes:
        template_file = self.environment.get_template(
            f"{template.value}/template.html"
        )

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
from flask import render_template

from stellar.blueprints.main import main_bp


@main_bp.get("/")
def index():
    return render_template(
        "main/index.html"
    )


@main_bp.get("/health")
async def health():
    from sqlalchemy import text

    from stellar.config.database import engine

    async with engine.connect() as connection:

        await connection.execute(
            text("SELECT 1")
        )

    return {
        "status": "ok",
        "database": "ok",
    }
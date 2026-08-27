from flask import (
    redirect,
    render_template,
    session,
    url_for,
)

from stellar.blueprints.cv import cv_bp


@cv_bp.get("/create")
async def create_cv():

    access_token = session.get(
        "access_token"
    )

    refresh_token = session.get(
        "refresh_token"
    )

    if not access_token or not refresh_token:

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "cv/create.html"
    )
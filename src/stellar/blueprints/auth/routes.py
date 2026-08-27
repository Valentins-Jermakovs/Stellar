from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from stellar.clients.meridian import MeridianClient, MeridianError


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
)


@auth_bp.get("/login")
async def login():
    return render_template("auth/login.html")


@auth_bp.post("/login")
async def login_submit():

    login = request.form.get("login", "").strip()
    password = request.form.get("password", "")

    if not login or not password:
        flash(
            "Login and password are required.",
            "error",
        )

        return redirect(
            url_for("auth.login")
        )

    client = MeridianClient()

    try:

        tokens = await client.login(
            login=login,
            password=password,
        )

    except MeridianError:

        flash(
            "Invalid login or password.",
            "error",
        )

        return redirect(
            url_for("auth.login")
        )

    session.clear()

    session["access_token"] = tokens.access_token
    session["refresh_token"] = tokens.refresh_token

    return redirect(
        url_for("auth.current_user")
    )


@auth_bp.get("/me")
async def current_user():

    access_token = session.get(
        "access_token"
    )

    if not access_token:

        return redirect(
            url_for("auth.login")
        )

    client = MeridianClient()

    try:

        user = await client.get_current_user(
            access_token
        )

    except MeridianError:

        session.clear()

        flash(
            "Your session has expired.",
            "error",
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "auth/me.html",
        user=user,
    )


@auth_bp.post("/logout")
async def logout():

    refresh_token = session.get(
        "refresh_token"
    )

    if refresh_token:

        client = MeridianClient()

        try:

            await client.logout(
                refresh_token
            )

        except MeridianError:
            pass

    session.clear()

    return redirect(
        url_for("main.index")
    )
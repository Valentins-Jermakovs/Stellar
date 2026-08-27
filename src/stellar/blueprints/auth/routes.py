from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from stellar.clients.meridian import (
    MeridianClient,
    MeridianError,
)


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
)


# ============================================================
# LOGIN
# ============================================================

@auth_bp.get("/login")
async def login():

    return render_template(
        "auth/login.html"
    )


@auth_bp.post("/login")
async def login_submit():

    login = request.form.get(
        "login",
        "",
    ).strip()

    password = request.form.get(
        "password",
        "",
    )

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

    session["access_token"] = (
        tokens.access_token
    )

    session["refresh_token"] = (
        tokens.refresh_token
    )

    return redirect(
        url_for("auth.current_user")
    )


# ============================================================
# REGISTER
# ============================================================

@auth_bp.get("/register")
async def register():

    return render_template(
        "auth/register.html"
    )


@auth_bp.post("/register")
async def register_submit():

    username = request.form.get(
        "username",
        "",
    ).strip()

    full_name = request.form.get(
        "full_name",
        "",
    ).strip()

    email = request.form.get(
        "email",
        "",
    ).strip()

    password = request.form.get(
        "password",
        "",
    )

    password_confirm = request.form.get(
        "password_confirm",
        "",
    )

    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    if not username:

        flash(
            "Username is required.",
            "error",
        )

        return redirect(
            url_for("auth.register")
        )

    if not full_name:

        flash(
            "Full name is required.",
            "error",
        )

        return redirect(
            url_for("auth.register")
        )

    if not email:

        flash(
            "Email is required.",
            "error",
        )

        return redirect(
            url_for("auth.register")
        )

    if not password:

        flash(
            "Password is required.",
            "error",
        )

        return redirect(
            url_for("auth.register")
        )

    if password != password_confirm:

        flash(
            "Passwords do not match.",
            "error",
        )

        return redirect(
            url_for("auth.register")
        )

    if len(password) < 8:

        flash(
            "Password must contain at least 8 characters.",
            "error",
        )

        return redirect(
            url_for("auth.register")
        )

    # --------------------------------------------------------
    # Create account
    # --------------------------------------------------------

    client = MeridianClient()

    try:

        await client.register(
            username=username,
            full_name=full_name,
            email=email,
            password=password,
        )

    except MeridianError:

        flash(
            "Unable to create account. "
            "Username or email may already be in use.",
            "error",
        )

        return redirect(
            url_for("auth.register")
        )

    # --------------------------------------------------------
    # Login after registration
    # --------------------------------------------------------

    try:

        tokens = await client.login(
            login=username,
            password=password,
        )

    except MeridianError:

        flash(
            "Account created successfully. "
            "Please sign in.",
            "success",
        )

        return redirect(
            url_for("auth.login")
        )

    session.clear()

    session["access_token"] = (
        tokens.access_token
    )

    session["refresh_token"] = (
        tokens.refresh_token
    )

    return redirect(
        url_for("auth.current_user")
    )


# ============================================================
# CURRENT USER
# ============================================================

@auth_bp.get("/me")
async def current_user():

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

    client = MeridianClient()

    try:

        user = await client.get_current_user(
            access_token
        )

    except MeridianError:

        session.clear()

        flash(
            "Your session has expired. "
            "Please sign in again.",
            "error",
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "auth/me.html",
        user=user,
    )


# ============================================================
# UPDATE CURRENT USER
# ============================================================

@auth_bp.post("/me/update")
async def update_current_user():

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

    username = request.form.get(
        "username",
        "",
    ).strip()

    full_name = request.form.get(
        "full_name",
        "",
    ).strip()

    email = request.form.get(
        "email",
        "",
    ).strip()

    current_password = request.form.get(
        "current_password",
        "",
    )

    password = request.form.get(
        "password",
        "",
    )

    password_confirm = request.form.get(
        "password_confirm",
        "",
    )

    # --------------------------------------------------------
    # Password validation
    # --------------------------------------------------------

    if password:

        if not current_password:

            flash(
                "Current password is required "
                "when changing your password.",
                "error",
            )

            return redirect(
                url_for("auth.current_user")
            )

        if password != password_confirm:

            flash(
                "New passwords do not match.",
                "error",
            )

            return redirect(
                url_for("auth.current_user")
            )

        if len(password) < 8:

            flash(
                "New password must contain "
                "at least 8 characters.",
                "error",
            )

            return redirect(
                url_for("auth.current_user")
            )

    # --------------------------------------------------------
    # Update
    # --------------------------------------------------------

    client = MeridianClient()

    try:

        await client.update_current_user(
            access_token,
            username=username or None,
            full_name=full_name or None,
            email=email or None,
            current_password=(
                current_password or None
            ),
            password=password or None,
        )

    except MeridianError as error:

        if error.status_code == 401:

            session.clear()

            flash(
                "Your session has expired. "
                "Please sign in again.",
                "error",
            )

            return redirect(
                url_for("auth.login")
            )

        flash(
            "Unable to update your profile.",
            "error",
        )

        return redirect(
            url_for("auth.current_user")
        )

    flash(
        "Your profile has been updated.",
        "success",
    )

    return redirect(
        url_for("auth.current_user")
    )


# ============================================================
# LOGOUT
# ============================================================

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


# ============================================================
# LOGOUT ALL
# ============================================================

@auth_bp.post("/logout-all")
async def logout_all():

    access_token = session.get(
        "access_token"
    )

    refresh_token = session.get(
        "refresh_token"
    )

    if not access_token or not refresh_token:

        session.clear()

        return redirect(
            url_for("auth.login")
        )

    client = MeridianClient()

    try:

        await client.logout_all(
            access_token
        )

    except MeridianError:

        session.clear()

        flash(
            "Unable to log out from all sessions.",
            "error",
        )

        return redirect(
            url_for("auth.login")
        )

    session.clear()

    flash(
        "You have been logged out from all sessions.",
        "success",
    )

    return redirect(
        url_for("auth.login")
    )
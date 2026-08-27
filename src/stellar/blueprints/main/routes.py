from flask import render_template

from stellar.blueprints.main import main_bp


@main_bp.route("/")
def index():
    return render_template("main/index.html")
from flask import Flask

from stellar.config.settings import settings


def create_app() -> Flask:

    app = Flask(__name__)

    app.config["SECRET_KEY"] = settings.FLASK_SECRET_KEY

    from stellar.blueprints.main import main_bp
    from stellar.blueprints.auth import auth_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    return app
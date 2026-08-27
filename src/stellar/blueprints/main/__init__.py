from flask import Blueprint


main_bp = Blueprint(
    "main",
    __name__,
)


from stellar.blueprints.main import routes
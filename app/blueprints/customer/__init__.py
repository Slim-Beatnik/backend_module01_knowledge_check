from flask import Blueprint

customer_bp = Blueprint("customer_bp", __name__)

from . import routes  # noqa: E402, F401

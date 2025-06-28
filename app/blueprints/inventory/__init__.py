from flask import Blueprint

inventory_bp = Blueprint("inventory_bp", __name__)

from . import routes  # noqa: E402, F401

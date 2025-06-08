from flask import Flask

from .blueprints.customer import customer_bp
from .extensions import ma
from .models import db


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f"config.{config_name}")

    # initialize extensions
    ma.init_app(app)
    db.init_app(app)

    # register blueprints
    app.register_blueprint(customer_bp, url_prefix="/customers")

    return app

from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from app.extensions import limiter

# app.models.get_all(table_class, many_schema)
from app.models import Mechanics, db, get_all

from . import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema


@mechanics_bp.route("/", methods=["POST"])
@limiter.limit("100 per month")
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_mechanic = Mechanics(**mechanic_data)
    db.session.add(new_mechanic)

    # opted for IntegrityError handling here the error message is more explicit
    # and would allow office admin to know how exactly what went wrong
    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": e.orig.args[1]}), 409

    return mechanic_schema.jsonify(new_mechanic), 201


@mechanics_bp.route("/", methods=["GET"])
# @cache.cached(timeout=30)
def get_mechanics():
    return get_all(Mechanics, mechanics_schema)


@mechanics_bp.route("/<int:mechanics_id>", methods=["PUT"])
def update_mechanics(mechanics_id):
    mechanics = db.session.get(Mechanics, mechanics_id)

    if not mechanics:
        return jsonify({"error": "Mechanic not found."}), 400

    try:
        mechanics_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in mechanics_data.items():
        setattr(mechanics, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanics), 200


@mechanics_bp.route("/<int:mechanics_id>", methods=["DELETE"])
@limiter.limit("50 per month")  # probably not firing over 50 employees
def delete_mechanics(mechanics_id):
    mechanic = db.session.get(Mechanics, mechanics_id)

    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 400

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify(
        {"message": f"Mechanic id: {mechanics_id}, successfully deleted."},
    ), 200

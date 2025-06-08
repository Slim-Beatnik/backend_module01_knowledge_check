from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select

from app.models import Mechanics, db

from . import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema


@mechanics_bp.route("/", methods=["POST"])
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_mechanic = Mechanics(**mechanic_data)
    db.session.add(new_mechanic)
    db.session.commit()

    return mechanic_schema.jsonify(new_mechanic), 201


@mechanics_bp.route("/", methods=["GET"])
def get_mechanics():
    query = select(Mechanics)
    mechanics = db.session.execute(query).scalars().all()

    if len(mechanics):
        return mechanics_schema.jsonify(mechanics), 200
    return jsonify({"error": "No mechanics found."}), 400


@mechanics_bp.route("/<int:mechanics_id>", methods=["PUT"])
def update_mechanics(mechanics_id):
    mechanics = db.session.get(Mechanics, mechanics_id)

    if not mechanics:
        return jsonify({"error": "Mechanic not found."}), 400

    try:
        mechanics_data = mechanics_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in mechanics_data.items():
        setattr(mechanics, key, value)

    db.session.commit()
    return mechanics_schema.jsonify(mechanics), 200


@mechanics_bp.route("/<int:mechanics_id>", methods=["DELETE"])
def delete_mechanics(mechanics_id):
    mechanics = db.session.get(Mechanics, mechanics_id)

    if not mechanics:
        return jsonify({"error": "Customer not found."}), 400

    db.session.delete(mechanics)
    db.session.commit()
    return jsonify(
        {"message": f"Customer id: {mechanics_id}, successfully deleted."},
    ), 200


# @mechanics_bp.route("/current_assignments", methods=["GET"])
# def get_all_current_assignments():
#     query = select(Mechanics).join(ServiceTickets).where(ServiceTickets.mechanics.any())
#     mechanics = db.session.execute(query).scalars().all()

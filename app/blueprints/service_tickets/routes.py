from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select

from app.models import Customer, Mechanics, ServiceTickets, db
from app.utils.util import token_required

from . import service_tickets_bp
from .schemas import service_ticket_schema, service_tickets_schema


@service_tickets_bp.route("/", methods=["POST"])
def create_service_ticket():
    data = request.get_json()

    # remove customer_id from data
    customer_id = data.pop("customer_id", None)
    if not customer_id:
        return jsonify({"error": "Customer ID is required."}), 400

    if not db.session.get(Customer, customer_id):
        return jsonify({"error": "Customer not found."}), 404

    try:
        service_ticket_data = service_ticket_schema.load(data)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_service_ticket = ServiceTickets(**service_ticket_data)
    new_service_ticket.customer_id = customer_id

    db.session.add(new_service_ticket)
    db.session.commit()

    return service_ticket_schema.jsonify(new_service_ticket), 201


@service_tickets_bp.route("/", methods=["GET"])
def get_all_service_tickets():
    query = select(ServiceTickets)
    service_tickets = db.session.execute(query).scalars().all()

    if len(service_tickets):
        return service_tickets_schema.jsonify(service_tickets), 200
    return jsonify(
        {"error": "No service tickets found."},
    ), 400


@service_tickets_bp.route("/<int:service_tickets_id>", methods=["GET"])
def get_service_ticket(service_tickets_id):
    service_tickets = db.session.get(ServiceTickets, service_tickets_id)

    if service_tickets:
        return service_ticket_schema.jsonify(service_tickets), 200
    return jsonify({"error": "Service ticket not found."}), 400


@service_tickets_bp.route("/my-tickets", methods=["GET"])
@token_required
def get_service_tickets_by_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    query = select(ServiceTickets).where(ServiceTickets.customer_id == customer_id)
    service_tickets = db.session.execute(query).scalars().all()

    if not service_tickets or not customer:
        return jsonify({"error": "Customer not found."}), 404

    return jsonify(service_tickets_schema.dump(service_tickets)), 200


@service_tickets_bp.route(
    "/<int:service_ticket_id>/assign-mechanic/<int:mechanic_id>",
    methods=["PUT"],
)
def assign_mechanic(service_ticket_id, mechanic_id):
    service_ticket = db.session.get(ServiceTickets, service_ticket_id)
    mechanic = db.session.get(Mechanics, mechanic_id)

    if not service_ticket or not mechanic:
        return jsonify({"error": "Service ticket or mechanic not found."}), 400
    if mechanic in service_ticket.mechanics:
        return jsonify(
            {
                "error": "This mechanic already assigned to this service ticket.",
            },
        ), 409
    service_ticket.mechanics.append(mechanic)
    db.session.commit()

    return service_ticket_schema.jsonify(service_ticket), 200


@service_tickets_bp.route(
    "/<int:service_ticket_id>/remove-mechanic/<int:mechanic_id>",
    methods=["PUT"],
)
def dismiss_mechanic(service_ticket_id, mechanic_id):
    service_ticket = db.session.get(ServiceTickets, service_ticket_id)
    mechanic = db.session.get(Mechanics, mechanic_id)
    print(service_ticket, mechanic)

    if not service_ticket or not mechanic:
        return jsonify({"error": "Service ticket or mechanic not found."}), 400
    if mechanic not in service_ticket.mechanics:
        return jsonify(
            {
                "error": "This mechanic isn't assigned to this service ticket.",
            },
        ), 409
    service_ticket.mechanics.remove(mechanic)
    db.session.commit()

    return service_ticket_schema.jsonify(service_ticket), 200

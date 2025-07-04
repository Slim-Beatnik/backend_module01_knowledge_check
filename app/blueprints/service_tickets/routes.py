from flask import g, jsonify, request
from marshmallow import ValidationError
from sqlalchemy import or_, select

# app.models.get_all(table_class, many_schema)
from app.models import Customer, Inventory, Mechanics, ServiceTickets, db, get_all
from app.utils.util import role_required, token_required

from . import service_tickets_bp
from .schemas import (
    edit_assigned_mechanics_schema,
    edit_inventory_schema,
    return_service_ticket_schema,
    service_ticket_schema,
    service_tickets_schema,
)


@service_tickets_bp.route("/", methods=["POST"])
@role_required
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
# @cache.cached(timeout=30)
@role_required
def get_service_tickets():
    return get_all(ServiceTickets, service_tickets_schema)


@service_tickets_bp.route("/<int:service_tickets_id>", methods=["GET"])
def get_service_ticket(service_tickets_id):
    service_tickets = db.session.get(ServiceTickets, service_tickets_id)

    if service_tickets:
        return service_ticket_schema.jsonify(service_tickets), 200
    return jsonify({"error": "Service ticket not found."}), 400


@service_tickets_bp.route("/<int:service_ticket_id>/edit-mechanics", methods=["PUT"])
@role_required
def edit_mechanics_assignments_by_service_ticket_id(service_ticket_id):
    try:
        st_edit_mechs = edit_assigned_mechanics_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    service_ticket = db.session.get(ServiceTickets, service_ticket_id)

    for mechanic_id in st_edit_mechs["add_mechanic_ids"]:
        mechanic = db.session.get(Mechanics, mechanic_id)

        if mechanic and mechanic not in service_ticket.mechanics:
            service_ticket.mechanics.append(mechanic)

    for mechanic_id in st_edit_mechs["remove_mechanic_ids"]:
        mechanic = db.session.get(Mechanics, mechanic_id)

        if mechanic and mechanic in service_ticket.mechanics:
            service_ticket.mechanics.remove(mechanic)
    db.session.commit()
    return return_service_ticket_schema.jsonify(service_ticket), 200


@service_tickets_bp.route("/<int:service_ticket_id>/edit-inventory", methods=["PUT"])
@role_required
def edit_inventory_by_service_ticket_id(service_ticket_id):
    try:
        st_edit_prods = edit_inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    service_ticket = db.session.get(ServiceTickets, service_ticket_id)

    for inventory_id in st_edit_prods["add_inventory_ids"]:
        inventory = db.session.get(Inventory, inventory_id)

        if inventory and inventory not in service_ticket.inventories:
            service_ticket.inventories.append(inventory)

    for inventory_id in st_edit_prods["remove_inventory_ids"]:
        inventory = db.session.get(Inventory, inventory_id)

        if inventory and inventory in service_ticket.inventories:
            service_ticket.inventories.remove(inventory)
    db.session.commit()
    return return_service_ticket_schema.jsonify(service_ticket), 200


# user based routes search
@service_tickets_bp.route("/my-tickets", methods=["GET"])
@token_required
def get_service_tickets_by_customer(customer_id):
    customer = db.session.get(Customer, customer_id)
    query = select(ServiceTickets).where(ServiceTickets.customer_id == customer_id)
    service_tickets = db.session.execute(query).scalars().all()

    if not service_tickets or not customer:
        return jsonify(
            {
                "error": "Service ticket or customer not found. It's entirely possible this customer has no tickets.",
            },
        ), 404

    return jsonify(service_tickets_schema.dump(service_tickets)), 200


@service_tickets_bp.route("/assigned-tickets/search", methods=["GET"])
@role_required
def search_assigned_service_tickets():
    queries = {
        "service_date": request.args.get("date"),
        "vin": request.args.get("vin"),
        "service_desc": request.args.get("description"),
        "any": request.args.get("any"),
    }
    mechanic_id = g.user_id
    # learned a thing or two about select objects
    # if no values in query select object initialized with customer_id
    stmt = select(ServiceTickets).where(
        ServiceTickets.mechanics.any(mechanic_id == Mechanics.id),
    )
    filters = []

    # Loop model columns matching provided queries -- skip 'any' and None values
    for key, value in queries.items():
        if key == "any" or not value:
            continue
        if key in ServiceTickets.__table__.columns:
            column = getattr(ServiceTickets, key)
            filters.append(column.like(f"%{value}%"))

    # Add 'any' search across multiple columns
    if queries.get("any"):
        qry = f"%{queries['any']}%"
        filters.append(
            or_(
                ServiceTickets.vin.like(qry),
                ServiceTickets.service_desc.like(qry),
                ServiceTickets.service_date.like(qry),
            ),
        )

    if filters:
        stmt = stmt.where(*filters)

    filtered_service_tickets = db.session.execute(stmt).scalars().all()

    if not filtered_service_tickets:
        return jsonify({"message": "Filters failed to yield results."}), 404

    return jsonify(service_tickets_schema.dump(filtered_service_tickets)), 200

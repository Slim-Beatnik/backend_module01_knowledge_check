from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError

from app.blueprints.customer.schemas import mechanic_view_customers_schema
from app.extensions import limiter

# app.models.get_all(table_class, many_schema)
from app.models import (
    Customer,
    Mechanics,
    db,
    get_all,
    service_tickets_has_mechanics,
)
from app.utils.util import encode_token, role_required

from . import mechanics_bp
from .schemas import (
    mechanic_schema,
    mechanics_schema,
    role_login_schema,
)


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


@mechanics_bp.route("/login", methods=["POST"])
def login():
    try:
        credentials = role_login_schema.load(request.json)
        username = credentials["email"]
        password = credentials["password"]
    except KeyError:
        return jsonify(
            {"messages": "Username and password required."},
        ), 400

    query = select(Mechanics).where(Mechanics.email == username)
    mechanic = db.session.execute(
        query,
    ).scalar_one_or_none()  # Query mechanics table for a mechanics with this email

    if (
        mechanic and mechanic.password == password
    ):  # if we have a mechanics associated with the mechanicsname, validate the password
        auth_token = encode_token(
            mechanic.id,
            "mechanic",
        )

        response = {
            "status": "success",
            "message": "Successfully Logged In",
            "auth_token": auth_token,
        }
        return jsonify(response), 200
    return jsonify({"messages": "Invalid email or password!"}), 401


@mechanics_bp.route("/", methods=["GET"])
# @cache.cached(timeout=30)
@role_required
def get_mechanics():
    return get_all(Mechanics, mechanics_schema)


@mechanics_bp.route("/top-mechanics", methods=["GET"])
def get_top_mechanics():
    limit = request.args.get("limit")
    count_st_id = func.Count(
        service_tickets_has_mechanics.c.service_ticket_id,
    )
    stmt = (
        select(
            Mechanics,
            count_st_id.label("ticket_count"),
        )
        .join(service_tickets_has_mechanics)
        .group_by(
            Mechanics.id,
        )
        .order_by(
            count_st_id.desc(),
        )
        .limit(limit or 3)
    )
    results = db.session.execute(stmt).all()
    top_mechanics = {}
    for index, (mechanic, ticket_count) in enumerate(results):
        top_mechanics[index + 1] = {
            "name": mechanic.name,
            "ticket_count": ticket_count,
        }
    return jsonify(top_mechanics), 200


@mechanics_bp.route("/<int:mechanic_id>", methods=["PUT"])
@role_required
def update_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanics, mechanic_id)

    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 400

    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in mechanic_data.items():
        setattr(mechanic, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200


@mechanics_bp.route("/current-customer-search", methods=["GET"])
@role_required
def search_for_customer():
    queries = {
        "id": request.args.get("id"),
        "name": request.args.get("name"),
        "email": request.args.get("email"),
        "phone": request.args.get("phone"),
        "any": request.args.get("any"),
    }

    # search non-deleted customers
    stmt = select(Customer).where(Customer.soft_delete.is_(False))
    filters = []

    # Loop model columns matching provided queries -- skip 'any' and None values
    for key, value in queries.items():
        if key == "any" or not value:
            continue
        if key in Customer.__table__.columns:
            column = getattr(Customer, key)
            filters.append(column.like(f"%{value}%"))

    # Add 'any' search across multiple columns
    if queries.get("any"):
        qry = f"%{queries['any']}%"
        filters.append(
            or_(
                Customer.name.like(qry),
                Customer.email.like(qry),
                Customer.phone.like(qry),
            ),
        )

    if filters:
        stmt = stmt.where(*filters)

    filtered_customers = db.session.execute(stmt).scalars().all()

    if not filtered_customers:
        return jsonify({"message": "Filters failed to yield results."}), 404

    return jsonify(
        {
            "result": mechanic_view_customers_schema.dump(filtered_customers),
        },
    ), 200


@mechanics_bp.route("/deleted-customer-search", methods=["GET"])
@role_required
def search_for_deleted_customer():
    queries = {
        "id": request.args.get("id"),
        "name": request.args.get("name"),
        "email": request.args.get("email"),
        "phone": request.args.get("phone"),
        "any": request.args.get("any"),
    }

    # search non-deleted customers
    stmt = select(Customer).where(Customer.soft_delete.is_(True))
    filters = []

    # Loop model columns matching provided queries -- skip 'any' and None values
    for key, value in queries.items():
        if key == "any" or not value:
            continue
        if key in Customer.__table__.columns:
            column = getattr(Customer, key)
            filters.append(column.like(f"%{value}%"))

    # Add 'any' search across multiple columns
    if queries.get("any"):
        qry = f"%{queries['any']}%"
        filters.append(
            or_(
                Customer.name.like(qry),
                Customer.email.like(qry),
                Customer.phone.like(qry),
            ),
        )

    if filters:
        stmt = stmt.where(*filters)

    filtered_customers = db.session.execute(stmt).scalars().all()

    if not filtered_customers:
        return jsonify({"message": "Filters failed to yield results."}), 404

    return jsonify(
        {
            "result": mechanic_view_customers_schema.dump(filtered_customers),
        },
    ), 200


@mechanics_bp.route("/<int:mechanics_id>", methods=["DELETE"])
@limiter.limit("5 per month")  # probably not firing over 50 employees
@role_required
def delete_mechanics(mechanics_id):
    mechanic = db.session.get(Mechanics, mechanics_id)

    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 400

    db.session.delete(mechanic)
    db.session.commit()
    return jsonify(
        {"message": f"Mechanic id: {mechanics_id}, successfully deleted."},
    ), 200

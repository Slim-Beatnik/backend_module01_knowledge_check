from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.extensions import cache, limiter

# app.models.get_all(table_class, many_schema)
from app.models import Customer, db, get_all
from app.utils.util import encode_token, token_required

from . import customer_bp
from .schemas import customer_schema, customers_schema, login_schema


@customer_bp.route("/login", methods=["POST"])
def login():
    try:
        credentials = login_schema.load(request.json)
        username = credentials["email"]
        password = credentials["password"]
    except KeyError:
        return jsonify(
            {"messages": "Invalid payload, expecting username and password"},
        ), 400

    query = select(Customer).where(Customer.email == username)
    customer = db.session.execute(
        query,
    ).scalar_one_or_none()  # Query customer table for a customer with this email

    if (
        customer and customer.password == password
    ):  # if we have a customer associated with the customername, validate the password
        auth_token = encode_token(customer.id)  # , customer.role.role_name)

        response = {
            "status": "success",
            "message": "Successfully Logged In",
            "auth_token": auth_token,
        }
        return jsonify(response), 200
    return jsonify({"messages": "Invalid email or password!"}), 401


@customer_bp.route("/", methods=["POST"])
@limiter.limit("5 per day")
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Customer).where(
        Customer.email == customer_data["email"],
    )  # Checking our db for a customer with this email
    existing_customer = db.session.execute(query).scalars().all()

    # opted to handle potential IntegrityError with simple error handling
    if existing_customer:
        return jsonify({"error": "Email already associated with an account."}), 400

    new_customer = Customer(**customer_data)

    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201


@customer_bp.route("/<int:customer_id>", methods=["GET"])
@cache.cached(timeout=600)
def get_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if customer:
        return customer_schema.jsonify(customer), 200
    return jsonify({"error": "Customer not found."}), 400


@customer_bp.route("/", methods=["GET"])
# @cache.cached(timeout=30)
def get_customers():
    return get_all(Customer, customers_schema)


@customer_bp.route("/", methods=["PUT"])
@limiter.limit("5 per day")
@token_required
def update_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"error": "Customer not found."}), 400

    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in customer_data.items():
        setattr(customer, key, value)

    db.session.commit()
    return customer_schema.jsonify(customer), 200


@customer_bp.route("/", methods=["DELETE"])
@token_required
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if not customer:
        return jsonify({"error": "Customer not found."}), 400

    db.session.delete(customer)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        customer.customer_removed_self = True
        db.session.commit()
        return jsonify(
            {
                "message": "Customer still attached to service tickets. Successfully marked for deletion",
            },
        ), 200

    return jsonify(
        {"message": f"Customer id: {customer_id}, successfully deleted."},
    ), 200

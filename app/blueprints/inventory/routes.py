from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy import or_, select

# from sqlalchemy.exc import IntegrityError
from app.extensions import cache, limiter

# app.models.get_all(table_class, many_schema)
from app.models import Inventory, db, get_all
from app.utils.util import role_required

from . import inventory_bp
from .schemas import inventories_schema, inventory_schema


@inventory_bp.route("/", methods=["POST"])
@role_required
def create_inventory():
    try:
        inventory_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    query = select(Inventory).where(
        Inventory.product_name == inventory_data["product_name"],
    )  # Checking our db for a inventory with this email
    existing_inventory = db.session.execute(query).scalars().first()

    # opted to handle potential IntegrityError with simple error handling
    if existing_inventory:
        return jsonify({"error": "Products require unique names for clarity."}), 400

    new_inventory = Inventory(**inventory_data)

    db.session.add(new_inventory)
    db.session.commit()
    return inventory_schema.jsonify(new_inventory), 201


# gets not protected for store front purposes
@inventory_bp.route("/<int:inventory_id>", methods=["GET"])
@cache.cached(timeout=600)
def get_inventory(inventory_id):
    inventory = db.session.get(Inventory, inventory_id)

    if inventory:
        return inventory_schema.jsonify(inventory), 200
    return jsonify({"error": "Inventory not found."}), 400


@inventory_bp.route("/", methods=["GET"])
@cache.cached(timeout=600)
def get_inventories():
    return get_all(Inventory, inventories_schema)


@inventory_bp.route("/search", methods=["GET"])
def search_inventories():
    queries = {
        "product_name": request.args.get("name"),
        "price": request.args.get("price"),
        "recalled": request.args.get("recalled"),
        "any": request.args.get("any"),
    }

    # learned a thing or two about select objects
    # if no values in query select object initialized with customer_id
    stmt = select(Inventory)
    filters = []

    # Loop model columns matching provided queries -- skip 'any' and None values
    for key, value in queries.items():
        if key == "any" or not value:
            continue
        if key in Inventory.__table__.columns:
            column = getattr(Inventory, key)
            filters.append(column.like(f"%{value}%"))

    # Add 'any' search across multiple columns
    if queries.get("any"):
        qry = f"%{queries['any']}%"
        filters.append(
            or_(
                Inventory.product_name.like(qry),
                Inventory.price.like(qry),
                Inventory.recalled.like(qry),
            ),
        )

    if filters:
        stmt = stmt.where(*filters)

    filtered_inventories = db.session.execute(stmt).scalars().all()

    if not filtered_inventories:
        return jsonify({"message": "Filters failed to yield results."}), 404

    return jsonify(inventories_schema.dump(filtered_inventories)), 200


@inventory_bp.route("/<int:inventory_id>", methods=["PUT"])
#
def update_inventory(inventory_id):
    inventory = db.session.get(Inventory, inventory_id)

    if not inventory:
        return jsonify({"error": "Inventory not found."}), 400

    try:
        inventory_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for key, value in inventory_data.items():
        setattr(inventory, key, value)

    db.session.commit()
    return inventory_schema.jsonify(inventory), 200


@inventory_bp.route("/<int:inventory_id>", methods=["DELETE"])
@limiter.limit("50 per month")  # probably not firing over 50 employees
def delete_inventory(inventory_id):
    inventory = db.session.get(Inventory, inventory_id)

    if not inventory:
        return jsonify({"error": "Inventory item not found."}), 400

    db.session.delete(inventory)
    db.session.commit()
    return jsonify(
        {"message": f"Inventory item id: {inventory_id}, successfully deleted."},
    ), 200

from datetime import date

from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# ============= MODELS ===============================================================
# order: Customer -> ServiceTickets -> Mechanics

service_tickets_has_mechanics = db.Table(
    "service_tickets_has_mechanics",
    Base.metadata,
    db.Column("service_ticket_id", db.ForeignKey("service_tickets.id")),
    db.Column("mechanic_id", db.ForeignKey("mechanics.id")),
)

service_tickets_has_inventories = db.Table(
    "service_tickets_has_inventories",
    Base.metadata,
    db.Column("service_ticket_id", db.ForeignKey("service_tickets.id")),
    db.Column("inventory_id", db.ForeignKey("inventory.id")),
    db.Column("quantity", db.Integer, default=1),
)


class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(11), nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    soft_delete: Mapped[bool] = mapped_column(default=False)

    service_tickets: Mapped[list["ServiceTickets"]] = db.relationship(
        back_populates="customer",
    )


class Inventory(Base):
    __tablename__ = "inventory"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(
        db.String(255),
        unique=True,
        nullable=False,
    )
    price: Mapped[float] = mapped_column(db.Float, nullable=False)
    # if recalled, easily get associated service tickets
    recalled: Mapped[bool] = mapped_column(db.Boolean, default=False)
    # regular consumables will be altered
    recallable: Mapped[bool] = mapped_column(db.Boolean, default=True)

    no_longer_used: Mapped[bool] = mapped_column(db.Boolean, default=False)

    service_tickets: Mapped[list["ServiceTickets"]] = db.relationship(
        secondary="service_tickets_has_inventories",
        back_populates="inventories",
    )


class Mechanics(Base):
    __tablename__ = "mechanics"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(10), nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)

    service_tickets: Mapped[list["ServiceTickets"]] = db.relationship(
        secondary="service_tickets_has_mechanics",
        back_populates="mechanics",
    )


class ServiceTickets(Base):
    __tablename__ = "service_tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    vin: Mapped[str] = mapped_column(db.String(17), nullable=False)
    service_date: Mapped[date] = mapped_column(db.Date)
    service_desc: Mapped[str] = mapped_column(db.String(255), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey("customer.id"))

    customer: Mapped["Customer"] = db.relationship(back_populates="service_tickets")
    mechanics: Mapped[list["Mechanics"]] = db.relationship(
        secondary="service_tickets_has_mechanics",
        back_populates="service_tickets",
    )
    inventories: Mapped[list["Inventory"]] = db.relationship(
        secondary="service_tickets_has_inventories",
        back_populates="service_tickets",
    )

    __table_args__ = (
        CheckConstraint("CHAR_LENGTH(vin) = 17", name="check_vin_length"),
    )


# helper function for get from any of the schemas where many=True
def get_all(table_class, many_schema, filter_property=None, filter_value=None):
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        query = select(table_class)
        if filter_property and filter_value:
            query = query.filter_by(filter_property.is_(filter_value))
        output_obj = db.paginate(query, page=page, per_page=per_page)
        return many_schema.jsonify(output_obj), 200
    except:  # noqa: E722
        query = select(table_class)
        output_obj = db.session.execute(query).scalars().all()
        return many_schema.jsonify(output_obj), 200

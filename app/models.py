from datetime import date

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# ============= MODELS ===============================================================
# order: Customer -> ServiceTickets -> Mechanics

service_mechanic = db.Table(
    "service_mechanic",
    Base.metadata,
    db.Column("service_ticket_id", db.ForeignKey("service_tickets.id")),
    db.Column("mechanic_id", db.ForeignKey("mechanics.id")),
)


class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(11), nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    customer_removed_self: Mapped[bool] = mapped_column(default=False)

    service_tickets: Mapped[list["ServiceTickets"]] = db.relationship(
        back_populates="customer",
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
        secondary="service_mechanic",
        back_populates="service_tickets",
    )

    __table_args__ = (
        CheckConstraint("CHAR_LENGTH(vin) = 17", name="check_vin_length"),
    )


class Mechanics(Base):
    __tablename__ = "mechanics"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(10), nullable=False)
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)

    service_tickets: Mapped[list["ServiceTickets"]] = db.relationship(
        secondary="service_mechanic",
        back_populates="mechanics",
    )

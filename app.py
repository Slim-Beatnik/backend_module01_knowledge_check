from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import List
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:test@localhost/repair_shop_db'


# Create a base class for our models
class Base(DeclarativeBase):
    pass

#Instantiate your SQLAlchemy database

db = SQLAlchemy(model_class = Base)
ma = Marshmallow()

db.init_app(app) #adding our db extension to our app
ma.init_app(app)

service_mechanic = db.Table(
    'service_mechanic',
    Base.metadata,
    db.Column('service_ticket_id', db.ForeignKey('service_tickets.id')),
    db.Column('mechanic_id', db.ForeignKey('mechanics.id'))
)

class Customer(Base):
    __tablename__ = 'customer'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(11), nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)

    service_tickets: Mapped[List['Service_Tickets']] = db.relationship(back_populates='customer')
    mechanics: Mapped[List['Mechanics']] = db.relationship(secondary='service_mechanic', back_populates='mechanics')
# Create the table


class Service_Tickets(Base):
    __tablename__ = 'service_tickets'

    id: Mapped[int] = mapped_column(primary_key=True)
    vin: Mapped[str] = mapped_column(db.String(17), nullable=False, unique=True)
    service_date: Mapped[date] = mapped_column(db.Date)
    service_desc: Mapped[str] = mapped_column(db.String(255), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('customer.id'))
    
    cusomter: Mapped['Customer'] = db.relationship(back_populates='service_tickets')
    
class Mechanics(Base):
    __tablename__ = "mechanics"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(11), nullable=False)
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)
    
    service_tickets: Mapped[List['Service_Tickets']] = db.relationship(secondary='service_mechanic', back_populates='service_tickets')
    
with app.app_context():
	db.create_all()
			
app.run(debug=True)
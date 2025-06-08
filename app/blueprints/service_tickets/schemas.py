from app.extensions import ma
from app.models import ServiceTickets


class ServiceTicketsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTickets


service_ticket_schema = ServiceTicketsSchema()
service_tickets_schema = ServiceTicketsSchema(many=True)

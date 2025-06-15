from marshmallow import fields

from app.extensions import ma
from app.models import ServiceTickets


class ServiceTicketsSchema(ma.SQLAlchemyAutoSchema):
    customer_id = fields.Int()
    mechanics = fields.Nested("MechanicsSchema", many=True)

    class Meta:
        model = ServiceTickets


class EditAssignedMechanicsSchema(ma.Schema):
    add_mechanic_ids = fields.List(fields.Int(), required=True)
    remove_mechanic_ids = fields.List(fields.Int(), required=True)

    class Meta:
        fields = ("add_mechanic_ids", "remove_mechanic_ids")


service_ticket_schema = ServiceTicketsSchema()
service_tickets_schema = ServiceTicketsSchema(many=True)
edit_assigned_mechanics_schema = EditAssignedMechanicsSchema()
return_service_ticket_schema = ServiceTicketsSchema(exclude=["customer_id"])

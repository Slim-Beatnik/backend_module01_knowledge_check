from marshmallow import fields

from app.blueprints.inventory.schemas import inventory_on_service_ticket_schema
from app.blueprints.mechanics.schemas import mechanics_on_service_ticket_schema
from app.extensions import ma
from app.models import ServiceTickets


class ServiceTicketsSchema(ma.SQLAlchemyAutoSchema):
    customer_id = fields.Int()
    mechanics = fields.Nested(mechanics_on_service_ticket_schema, many=True)
    inventories = fields.Nested(inventory_on_service_ticket_schema, many=True)

    class Meta:
        model = ServiceTickets


class EditAssignedMechanicsSchema(ma.Schema):
    add_mechanic_ids = fields.List(fields.Int(), required=True)
    remove_mechanic_ids = fields.List(fields.Int(), required=True)

    class Meta:
        fields = ("add_mechanic_ids", "remove_mechanic_ids")


class EditInventorySchema(ma.Schema):
    add_inventory_ids = fields.List(fields.Int(), required=True)
    remove_inventory_ids = fields.List(fields.Int(), required=True)

    class Meta:
        fields = ("add_inventory_ids", "remove_inventory_ids")


service_ticket_schema = ServiceTicketsSchema()
service_tickets_schema = ServiceTicketsSchema(many=True)
edit_assigned_mechanics_schema = EditAssignedMechanicsSchema()
edit_inventory_schema = EditInventorySchema()
return_service_ticket_schema = ServiceTicketsSchema(exclude=["customer_id"])

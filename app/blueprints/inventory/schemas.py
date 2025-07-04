from app.extensions import ma
from app.models import Inventory


class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory


inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)
inventory_on_service_ticket_schema = InventorySchema(
    only=("product_name", "price"),
    many=True,
)
shop_inventories_schema = InventorySchema(only=("product_name", "price"), many=True)
shop_inventory_schema = InventorySchema(only=("product_name", "price"))

from app.extensions import ma
from app.models import Mechanics


class MechanicsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanics


mechanic_schema = MechanicsSchema()
mechanics_schema = MechanicsSchema(many=True)

mechanics_on_service_ticket_schema = MechanicsSchema(
    only=("id", "name", "phone"),
    many=True,
)
role_login_schema = MechanicsSchema(only=("email", "password"))

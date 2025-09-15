# backend/api/roles.py
from flask.views import MethodView
from flask_smorest import Blueprint
from ..models import SystemRole
from ..schemas import SystemRoleSchema

blp = Blueprint("roles", __name__, description="System roles")

@blp.route("/")
class RolesList(MethodView):
    @blp.response(200, SystemRoleSchema(many=True))
    def get(self):
        return SystemRole.query.order_by(SystemRole.id.asc()).all()

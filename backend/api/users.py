# backend/api/users.py
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from ..db import db
from ..models import User, UserStatus
from ..schemas import UserSchema, UserCreateSchema, UserUpdateSchema
from .common import get_pagination
from marshmallow import Schema, fields

blp = Blueprint("users", __name__, description="Users CRUD")

class DeleteResponseSchema(Schema):
    deleted = fields.Boolean(required=True)

@blp.route("/")
class UsersList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        page, size = get_pagination()
        page_obj = User.query.order_by(User.id.asc()).paginate(page=page, per_page=size, error_out=False)
        return page_obj.items

    @blp.arguments(UserCreateSchema)
    @blp.response(201, UserSchema)
    def post(self, data):
        u = User(
            name=data["name"],
            email=data["email"],
            role_id=data["role_id"],
            status=UserStatus(data["status"]),
            cohort_id=data.get("cohort_id"),
            subgroup_id=data.get("subgroup_id"),
        )
        db.session.add(u); db.session.commit()
        return u

@blp.route("/<int:user_id>")
class UserResource(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id: int):
        u = User.query.get(user_id)
        if not u: abort(404, message="User not found")
        return u

    @blp.arguments(UserUpdateSchema)
    @blp.response(200, UserSchema)
    def put(self, data, user_id: int):
        u = User.query.get(user_id)
        if not u: abort(404, message="User not found")
        for k, v in data.items():
            setattr(u, k, UserStatus(v) if k == "status" else v)
        db.session.commit()
        return u

    @blp.response(200, DeleteResponseSchema)
    def delete(self, user_id: int):
        u = User.query.get(user_id)
        if not u: abort(404, message="User not found")
        db.session.delete(u); db.session.commit()
        return {"deleted": True}

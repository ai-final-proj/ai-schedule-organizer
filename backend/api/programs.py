# backend/api/programs.py
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from .schemas.common import DeleteResponseSchema

from ..db import db
from ..models import Program
from ..schemas import ProgramSchema, ProgramCreateSchema, ProgramUpdateSchema
from .common import get_pagination

blp = Blueprint("programs", __name__, description="Programs CRUD")

program_schema = ProgramSchema()

@blp.route("/")
class ProgramsList(MethodView):
    @blp.response(200, ProgramSchema(many=True))
    def get(self):
        page, size = get_pagination()
        q = Program.query.order_by(Program.id.asc()).paginate(page=page, per_page=size, error_out=False)
        return [program_schema.dump(p) for p in q.items]

    @blp.arguments(ProgramCreateSchema)
    @blp.response(201, ProgramSchema)
    def post(self, data):
        p = Program(name=data["name"], description=data.get("description"))
        db.session.add(p)
        db.session.commit()
        return program_schema.dump(p)

@blp.route("/<int:program_id>")
class ProgramResource(MethodView):
    @blp.response(200, ProgramSchema)
    def get(self, program_id: int):
        p = Program.query.get(program_id)
        if not p:
            abort(404, message="Program not found")
        return program_schema.dump(p)

    @blp.arguments(ProgramUpdateSchema)
    @blp.response(200, ProgramSchema)
    def put(self, data, program_id: int):
        p = Program.query.get(program_id)
        if not p:
            abort(404, message="Program not found")
        for k, v in data.items():
            setattr(p, k, v)
        db.session.commit()
        return program_schema.dump(p)

    @blp.response(200, DeleteResponseSchema)
    def delete(self, program_id: int):
        p = Program.query.get(program_id)
        if not p:
            abort(404, message="Program not found")
        db.session.delete(p)
        db.session.commit()
        return {"deleted": True}

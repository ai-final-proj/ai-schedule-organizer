# backend/api/cohorts.py
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from ..db import db
from ..models import Cohort, CohortSubgroup
from ..schemas import (
    CohortSchema, CohortCreateSchema, CohortUpdateSchema,
    CohortSubgroupSchema, SubgroupCreateSchema
)
from .common import get_pagination
from marshmallow import Schema, fields

blp = Blueprint("cohorts", __name__, description="Cohorts & subgroups")

class DeleteResponseSchema(Schema):
    deleted = fields.Boolean(required=True)

@blp.route("/")
class CohortsList(MethodView):
    @blp.response(200, CohortSchema(many=True))
    def get(self):
        page, size = get_pagination()
        page_obj = Cohort.query.order_by(Cohort.id.asc()).paginate(page=page, per_page=size, error_out=False)
        return page_obj.items

    @blp.arguments(CohortCreateSchema)
    @blp.response(201, CohortSchema)
    def post(self, data):
        c = Cohort(name=data["name"], description=data.get("description"))
        db.session.add(c); db.session.commit()
        return c

@blp.route("/<int:cohort_id>")
class CohortResource(MethodView):
    @blp.response(200, CohortSchema)
    def get(self, cohort_id: int):
        c = Cohort.query.get(cohort_id)
        if not c: abort(404, message="Cohort not found")
        return c

    @blp.arguments(CohortUpdateSchema)
    @blp.response(200, CohortSchema)
    def put(self, data, cohort_id: int):
        c = Cohort.query.get(cohort_id)
        if not c: abort(404, message="Cohort not found")
        for k, v in data.items():
            setattr(c, k, v)
        db.session.commit()
        return c

    @blp.response(200, DeleteResponseSchema)
    def delete(self, cohort_id: int):
        c = Cohort.query.get(cohort_id)
        if not c: abort(404, message="Cohort not found")
        db.session.delete(c); db.session.commit()
        return {"deleted": True}

@blp.route("/<int:cohort_id>/subgroups")
class Subgroups(MethodView):
    @blp.response(200, CohortSubgroupSchema(many=True))
    def get(self, cohort_id: int):
        c = Cohort.query.get(cohort_id)
        if not c: abort(404, message="Cohort not found")
        return CohortSubgroup.query.filter_by(cohort_id=cohort_id).all()

    @blp.arguments(SubgroupCreateSchema)
    @blp.response(201, CohortSubgroupSchema)
    def post(self, data, cohort_id: int):
        c = Cohort.query.get(cohort_id)
        if not c: abort(404, message="Cohort not found")
        sg = CohortSubgroup(name=data["name"], cohort_id=cohort_id)
        db.session.add(sg); db.session.commit()
        return sg

# backend/api/schedules.py
from datetime import datetime
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from .schemas.common import DeleteResponseSchema
from ..db import db
from ..models import (
    Schedule, ScheduleItem, Program, Cohort, CohortSubgroup,
    Period, PeriodCategory, User
)
from ..schemas import (
    ScheduleSchema, ScheduleCreateSchema, ScheduleUpdateSchema,
    ScheduleItemSchema, PeriodSchema, PeriodCreateSchema
)
from .common import get_pagination

blp = Blueprint("schedules", __name__, description="Schedules, periods, and items")

def _schedule_dict(s: Schedule):
    return {
        "id": s.id,
        "name": s.name,
        "description": s.description,
        "program_id": s.program_id,
        "cohort_id": s.cohort_id,
        "subgroup_id": s.subgroup_id,
        "program": {"id": s.program.id, "name": s.program.name} if s.program else None,
        "cohort": s.cohort.name if s.cohort else None,
        "subgroup": s.subgroup.name if s.subgroup else None,
    }

@blp.route("/schedules")
class SchedulesList(MethodView):
    @blp.response(200, ScheduleSchema(many=True))
    def get(self):
        page, size = get_pagination()
        page_obj = Schedule.query.order_by(Schedule.id.asc()).paginate(page=page, per_page=size, error_out=False)

        return [_schedule_dict(s) for s in page_obj.items]

    @blp.arguments(ScheduleCreateSchema)
    @blp.response(201, ScheduleSchema)
    def post(self, data):
        s = Schedule(**data)
        db.session.add(s); db.session.commit()
        return _schedule_dict(s)

@blp.route("/schedules/<int:schedule_id>")
class ScheduleResource(MethodView):
    @blp.response(200, Schema.from_dict({
        "schedule": fields.Nested(ScheduleSchema),
        "periods": fields.List(fields.Nested(PeriodSchema)),
    })())
    def get(self, schedule_id: int):
        s = Schedule.query.get(schedule_id)
        if not s: abort(404, message="Schedule not found")
        items = ScheduleItem.query.filter_by(schedule_id=s.id).all()
        periods = sorted({it.period for it in items if it.period}, key=lambda x: x.id)
        return {
            "schedule": _schedule_dict(s),
            "periods": periods,
        }

    @blp.arguments(ScheduleUpdateSchema)
    @blp.response(200, ScheduleSchema)
    def put(self, data, schedule_id: int):
        s = Schedule.query.get(schedule_id)
        if not s: abort(404, message="Schedule not found")
        for k, v in data.items():
            setattr(s, k, v)
        db.session.commit()
        return _schedule_dict(s)

    @blp.response(200, DeleteResponseSchema)
    def delete(self, schedule_id: int):
        s = Schedule.query.get(schedule_id)
        if not s: abort(404, message="Schedule not found")
        db.session.delete(s); db.session.commit()
        return {"deleted": True}

@blp.route("/schedule-items")
class ItemsList(MethodView):
    @blp.response(200, ScheduleItemSchema(many=True))
    def get(self):
        page, size = get_pagination()
        page_obj = ScheduleItem.query.order_by(ScheduleItem.id.asc()).paginate(page=page, per_page=size, error_out=False)
        return page_obj.items

    @blp.arguments(ScheduleItemSchema)
    @blp.response(201, ScheduleItemSchema)
    def post(self, data):
        for fld in ("start_date", "end_date"):
            if isinstance(data.get(fld), str):
                data[fld] = datetime.fromisoformat(data[fld])
        it = ScheduleItem(**data)
        db.session.add(it); db.session.commit()
        return it

@blp.route("/schedule-items/<int:item_id>")
class ItemResource(MethodView):
    @blp.response(200, DeleteResponseSchema)
    def delete(self, item_id: int):
        it = ScheduleItem.query.get(item_id)
        if not it: abort(404, message="Schedule item not found")
        db.session.delete(it); db.session.commit()
        return {"deleted": True}

@blp.route("/periods")
class PeriodsList(MethodView):
    @blp.response(200, PeriodSchema(many=True))
    def get(self):
        page, size = get_pagination()
        page_obj = Period.query.order_by(Period.id.asc()).paginate(page=page, per_page=size, error_out=False)
        return page_obj.items

    @blp.arguments(PeriodCreateSchema)
    @blp.response(201, PeriodSchema)
    def post(self, data):
        if data.get("instructor_id") and not User.query.get(data["instructor_id"]):
            abort(400, message="Instructor not found")

        p = Period(
            name=data["name"],
            description=data.get("description"),
            instructor_id=data.get("instructor_id"),
            location_url=data.get("location_url"),
            capacity=data.get("capacity"),
            category=PeriodCategory(data["category"]),
        )
        db.session.add(p); db.session.commit()
        return p

@blp.route("/periods/<int:period_id>")
class PeriodResource(MethodView):
    @blp.response(200, DeleteResponseSchema)
    def delete(self, period_id: int):
        p = Period.query.get(period_id)
        if not p: abort(404, message="Period not found")
        db.session.delete(p); db.session.commit()
        return {"deleted": True}

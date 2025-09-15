from marshmallow import Schema, fields

class ScheduleSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    program_id = fields.Int(allow_none=True)
    cohort_id = fields.Int(allow_none=True)
    subgroup_id = fields.Int(allow_none=True)
    program = fields.Dict(dump_only=True)  # {id,name}
    cohort = fields.Str(allow_none=True, dump_only=True)
    subgroup = fields.Str(allow_none=True, dump_only=True)

class ScheduleCreateSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    program_id = fields.Int(allow_none=True)
    cohort_id = fields.Int(allow_none=True)
    subgroup_id = fields.Int(allow_none=True)

class ScheduleUpdateSchema(Schema):
    name = fields.Str()
    description = fields.Str(allow_none=True)
    program_id = fields.Int(allow_none=True)
    cohort_id = fields.Int(allow_none=True)
    subgroup_id = fields.Int(allow_none=True)

class ScheduleItemSchema(Schema):
    id = fields.Int()
    schedule_id = fields.Int(required=True)
    program_id = fields.Int(allow_none=True)
    period_id = fields.Int(allow_none=True)
    cohort_id = fields.Int(allow_none=True)
    subgroup_id = fields.Int(allow_none=True)
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)

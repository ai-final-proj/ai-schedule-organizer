from marshmallow import Schema, fields, validate

class PeriodSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    instructor_id = fields.Int(allow_none=True)
    instructor = fields.Str(allow_none=True, dump_only=True)
    location_url = fields.Str(allow_none=True)
    capacity = fields.Int(allow_none=True)
    category = fields.Str(required=True, validate=validate.OneOf([
        "virtual_reality","face_to_face","assessment","learning_course","other"
    ]))

class PeriodCreateSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    instructor_id = fields.Int(allow_none=True)
    location_url = fields.Str(allow_none=True)
    capacity = fields.Int(allow_none=True)
    category = fields.Str(required=True, validate=validate.OneOf([
        "virtual_reality","face_to_face","assessment","learning_course","other"
    ]))

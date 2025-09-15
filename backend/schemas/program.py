from marshmallow import Schema, fields

class ProgramSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)

class ProgramCreateSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)

class ProgramUpdateSchema(Schema):
    name = fields.Str()
    description = fields.Str(allow_none=True)

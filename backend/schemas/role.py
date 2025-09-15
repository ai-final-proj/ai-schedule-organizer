from marshmallow import Schema, fields

class SystemRoleSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    code = fields.Str(required=True)

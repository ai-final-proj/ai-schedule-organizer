from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    role_id = fields.Int(required=True)
    status = fields.Str(validate=validate.OneOf(["active", "inactive"]))
    cohort = fields.Str(allow_none=True)
    subgroup = fields.Str(allow_none=True)

class UserCreateSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    role_id = fields.Int(required=True)
    status = fields.Str(load_default="active", validate=validate.OneOf(["active", "inactive"]))
    cohort_id = fields.Int(allow_none=True)
    subgroup_id = fields.Int(allow_none=True)

class UserUpdateSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    role_id = fields.Int()
    status = fields.Str(validate=validate.OneOf(["active", "inactive"]))
    cohort_id = fields.Int(allow_none=True)
    subgroup_id = fields.Int(allow_none=True)

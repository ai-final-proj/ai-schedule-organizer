from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    role_id = fields.Int(required=True)
    # Expose human-friendly names for related entities
    role = fields.Function(lambda obj: getattr(getattr(obj, "role", None), "name", None))
    cohort = fields.Function(lambda obj: getattr(getattr(obj, "cohort", None), "name", None))
    subgroup = fields.Function(lambda obj: getattr(getattr(obj, "subgroup", None), "name", None))
    # Ensure enums serialize to their value ("active" | "inactive")
    status = fields.Function(lambda obj: getattr(getattr(obj, "status", None), "value", None))

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

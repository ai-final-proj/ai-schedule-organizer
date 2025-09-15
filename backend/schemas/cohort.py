from marshmallow import Schema, fields

class CohortSubgroupSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    cohort_id = fields.Int(required=True)

class CohortSchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    subgroups = fields.List(fields.Nested(CohortSubgroupSchema), dump_only=True)

class CohortCreateSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)

class CohortUpdateSchema(Schema):
    name = fields.Str()
    description = fields.Str(allow_none=True)

class SubgroupCreateSchema(Schema):
    name = fields.Str(required=True)

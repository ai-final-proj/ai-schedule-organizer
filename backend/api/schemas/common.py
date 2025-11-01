from marshmallow import Schema, fields

class DeleteResponseSchema(Schema):
    deleted = fields.Boolean(required=True)
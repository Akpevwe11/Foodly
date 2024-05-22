from marshmallow import Schema, fields

class ProductSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    price = fields.Float(required=True)
    quantity = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class ProductUpdateSchema(Schema):
    name = fields.Str()
    description = fields.Str()
    price = fields.Float()
    quantity = fields.Int()


class OrderSchema(Schema):
    id = fields.Str(dump_only=True)
    product_id = fields.Str(required=True)
    quantity = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class OrderUpdateSchema(Schema):
    product_id = fields.Str()
    quantity = fields.Int()
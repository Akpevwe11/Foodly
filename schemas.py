from marshmallow import Schema, fields, validate



class PlainProductSchema(Schema):
    id = fields.Str(dump_only=True, required=True, validate=validate.Length(min=1))
    name = fields.Str(required=True, validate=validate.Length(min=2))
    description = fields.Str(required=True, validate=validate.Length(min=10))
    price = fields.Float(required=True, validate=validate.Range(min=0))
    quantity = fields.Int(required=True, validate=validate.Range(min=1))
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)




class ProductUpdateSchema(Schema):
    product_id = fields.Str(required=True, validate=validate.Length(min=1))
    name = fields.Str()
    description = fields.Str(validate=validate.Length(min=10))
    price = fields.Float(validate=validate.Range(min=0))
    quantity = fields.Int(validate=validate.Range(min=1))


class OrderSchema(Schema):
    id = fields.Str(dump_only=True)
    product_id = fields.Str(required=True)
    quantity = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class OrderUpdateSchema(Schema):
    product_id = fields.Str()
    quantity = fields.Int()


class PlainShopSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    address = fields.Str(required=True)
    phone = fields.Str(required=True)
    email = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ShopSchema(PlainShopSchema):
    products = fields.List(fields.Nested(PlainProductSchema(), dump_only=True))


class ProductSchema(PlainProductSchema):
    shop_id = fields.Str(required=True)
    shop = fields.Nested(PlainShopSchema(), dump_only=True)

class UserSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
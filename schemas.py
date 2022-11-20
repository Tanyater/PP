from flask_bcrypt import generate_password_hash
from marshmallow import validate, Schema, fields
from models import *


class Users(Schema):
	id = fields.Integer()
	username = fields.String()
	first_name = fields.String()
	last_name = fields.String()
	email = fields.String(validate=validate.Email())
	password = fields.String()
	phone = fields.String()


class UserNoid(Schema):
	username = fields.String()
	first_name = fields.String()
	last_name = fields.String()
	email = fields.String(validate=validate.Email())
	password = fields.Function(deserialize=lambda obj: generate_password_hash(obj), load_only=True)
	phone = fields.String()


class WalletNoid(Schema):
	money = fields.Float(validate=validate.Range(0))
	name = fields.String()
	currency = fields.String(validate=validate.OneOf(["EUR", "USD", "UAH"]))
	status = fields.String(validate=validate.OneOf(["active", "blocked"]))
	user_id = fields.Integer()


class WalletForPut(Schema):
	name = fields.String()
	money = fields.Float()
	currency = fields.String(validate=validate.OneOf(["EUR", "USD", "UAH"]))
	status = fields.String(validate=validate.OneOf(["active", "blocked"]))


class Wallets(Schema):
	id = fields.Integer()
	userId = fields.Integer()
	money = fields.Float()
	name = fields.String()
	currency = fields.String(validate=validate.OneOf(["EUR", "USD", "UAH"]))
	status = fields.String(validate=validate.OneOf(["active", "blocked"]))


class Transfers(Schema):
	id = fields.Integer()
	fromUserId = fields.Integer()
	fromWalletId = fields.Integer()
	toWalletId = fields.Integer()
	money = fields.Float()
	currency = fields.String(validate=validate.OneOf(["UAH"]))
	complete = fields.Boolean()


class TransferForUser(Schema):
	money = fields.Float(validate=validate.Range(0))
	currency = fields.String(validate=validate.OneOf(["UAH"]))
	complete = fields.Boolean()
	from_user_id = fields.Integer()
	from_wallet_id = fields.Integer()
	to_wallet_id = fields.Integer()





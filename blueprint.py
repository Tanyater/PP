from flask import Blueprint, jsonify, request, make_response
import sqlalchemy
import db_utils
import marshmallow
from models import User, Wallet, Transfer
from schemas import(
    Transfers,
    TransferForUser,
    UserNoid,
    Users,
    WalletNoid,
    WalletForPut,
    Wallets
)


api_blueprint = Blueprint('api', __name__)


@api_blueprint.route("/user", methods=["POST"])
def create_user():
    try:
        user_data = UserNoid().load(request.json)
        user = db_utils.create_entry(User, **user_data)
        response = make_response(jsonify(Users().dump(user)))
        response.status_code = 200
    except sqlalchemy.exc.IntegrityError as e:
        response = make_response(jsonify(message="Invalid data input", status=400))
        response.status_code = 400
    except marshmallow.exceptions.ValidationError as e:
        response = make_response(jsonify(message=e.args[0], status=400))
        response.status_code = 400
    return response


@api_blueprint.route("/user/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    try:
        user = db_utils.get_entry_by_id(User, user_id)
        response = make_response(jsonify(UserNoid().dump(user)))
        response.status_code = 200
    except sqlalchemy.exc.NoResultFound as e:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    return response


@api_blueprint.route("/user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        user_data = UserNoid().load(request.json)
        user = db_utils.get_entry_by_id(User, user_id)
        db_utils.update_entry(user, **user_data)
        response = make_response(jsonify(UserNoid().dump(user)))
        response.status_code = 200
    except marshmallow.exceptions.ValidationError as e:
        response = make_response(jsonify(message=e.args[0], status=400))
        response.status_code = 400
    except sqlalchemy.exc.NoResultFound as e:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    return response


@api_blueprint.route("/user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        db_utils.delete_entry(User, user_id)
        response = make_response(jsonify("User deleted"))
        response.status_code = 200
    except sqlalchemy.exc.IntegrityError as e:
        response = make_response(jsonify(message="User has wallets", status=400))
        response.status_code = 400
    except sqlalchemy.exc.NoResultFound as e:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    return response


@api_blueprint.route("/wallet", methods=["POST"])
def create_wallet():
    try:
        wallet_data = WalletNoid().load(request.json)
        wallet = db_utils.create_entry_wallet(Wallet, **wallet_data)
        response = make_response(jsonify(message="Wallet has been created", status=200))
        response.status_code = 200
    except sqlalchemy.exc.IntegrityError as e:
        response = make_response(jsonify(message="Invalid data input", status=400))
        response.status_code = 400
    except marshmallow.exceptions.ValidationError as e:
        response = make_response(jsonify(message=e.args[0], status=400))
        response.status_code = 400
    return response


@api_blueprint.route("/wallet/<int:id>", methods=["PUT"])
def update_wallet(id):
    try:
        wallet_data = WalletForPut().load(request.json)
        wallet = db_utils.get_entry_by_id(Wallet, id)
        db_utils.update_entry(wallet, **wallet_data)
        response = make_response(jsonify(WalletForPut().dump(wallet)))
        response.status_code = 200
    except sqlalchemy.exc.IntegrityError as e:
        response = make_response(jsonify(message="Invalid data input", status=400))
        response.status_code = 400
    except sqlalchemy.exc.NoResultFound as e:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    return response


@api_blueprint.route("/wallet/<int:id>", methods=["GET"])
def get_wallet_by_id(id):
    try:
        wallet = db_utils.get_entry_by_id(Wallet, id)
        response = make_response(jsonify(WalletNoid().dump(wallet)))
        response.status_code = 200
    except sqlalchemy.exc.NoResultFound as e:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    return response


@api_blueprint.route("/wallet/<int:id>", methods=["DELETE"])
def delete_wallet(id):
    try:
        db_utils.delete_entry(Wallet, id)
        response = make_response(jsonify("Wallet deleted"))
        response.status_code = 200
    except sqlalchemy.exc.IntegrityError as e:
        response = make_response(jsonify(message="Wallet is in transfer", status=400))
        response.status_code = 400
    except sqlalchemy.exc.NoResultFound as e:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    return response


@api_blueprint.route("/wallet/<status>", methods=['GET'])
def get_wallet_by_status(status):
    try:
        wallet = db_utils.get_entry_by_status(Wallet, status)
        response = make_response(jsonify(WalletNoid(many=True).dump(wallet)))
        response.status_code = 200
    except sqlalchemy.exc.IntegrityError as e:
        response = make_response(jsonify(message="Invalid status input", status=400))
        response.status_code = 400
    return response


@api_blueprint.route("/transfer", methods=["POST"])
def create_transfer():
    try:
        transfer_data = TransferForUser().load(request.json)
        transfer = db_utils.create_entry_transfer(Transfer, **transfer_data)
        response = make_response(jsonify(message="Transfer has been created", status=200))
        response.status_code = 200
    except sqlalchemy.exc.IntegrityError as e:
        response = make_response(jsonify(message="Invalid data input", status=400))
        response.status_code = 400
    except marshmallow.exceptions.ValidationError as e:
        response = make_response(jsonify(message=e.args[0], status=400))
        response.status_code = 400
    return response


@api_blueprint.route("/transfer/<int:id>", methods=["GET"])
def get_transfer_by_id(id):
    try:
        transfer = db_utils.get_entry_by_id(Transfer, id)
        response = make_response(jsonify(TransferForUser().dump(transfer)))
        response.status_code = 200
    except sqlalchemy.exc.NoResultFound as e:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    return response


@api_blueprint.route("/transfer/user/<int:user_id>", methods=["GET"])
def get_transfer_by_user_id(user_id):
    try:
        transfer = db_utils.get_entry_by_user_id(Transfer, user_id)
        response = make_response(jsonify(TransferForUser(many=True).dump(transfer)))
        response.status_code = 200
    except sqlalchemy.exc.IntegrityError as e:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    return response


@api_blueprint.route("/transfer/<int:id>", methods=["DELETE"])
def delete_transfer(id):
    if db_utils.get_entry_scalar(Transfer, id) is None:
        response = make_response(jsonify("Invalid id"))
        response.status_code = 400
        return response
    db_utils.delete_entry(Transfer, id)
    response = make_response(jsonify("Transfer deleted"))
    response.status_code = 200
    return response


#@api_blueprint.errorhandler(404)
#def server_error(e):
   # return jsonify(message="Invalid URL provided"), 404


#@api_blueprint.errorhandler(500)
#def server_error(e):
    #return jsonify(message="Invalid data provided"), 500
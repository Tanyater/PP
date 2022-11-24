from flask import Blueprint, jsonify, request, make_response, Flask, Response

import db_utils
from models import *
from db_utils import *
from schemas import *
from functools import wraps
from flask_cors import CORS
from werkzeug.security import check_password_hash
from flask_httpauth import HTTPBasicAuth
import marshmallow
import sqlalchemy

api_blueprint = Blueprint('user', __name__)
errors = Blueprint('errors', __name__)


auth = HTTPBasicAuth()
app = Flask(__name__)


@auth.verify_password
def verify_password(u_email, u_password):
    session = Session()
    persons = session.query(User)
    user_to_verify = db_utils.get_entry_by_email(User, u_email)
    if not user_to_verify:
        return None  # make_response('couldnt verify your login or password!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
    if check_password_hash(user_to_verify.password, u_password):
        print("email: " + u_email + ", password: " + u_password)
        return user_to_verify
    else:
        return None  # make_response('couldnt verify your login or password!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})


@auth.error_handler
def auth_error_handler(status):
    #if status == 401:
    #    message = "Wrong email or password"
    if status == 403:
        message = "Access denied"
    else:
        message = "Wrong email or password"
    return {"code": status, "message": message}, status


@auth.get_user_roles
def get_user_roles(user_to_get_role):
    print(user_to_get_role.role)
    return user_to_get_role.role
def dump_or_404(data, Schema):
    if data == 404:
        return Response("Invalid id", status=404)
    else:
        if isinstance(data, list):
            return jsonify(Schema.dump(data, many=True))
        return jsonify(Schema.dump(data))


@app.route('/user/login', methods=['POST'])
@auth.login_required(role=['admin', 'customuser'])
def login():
    return jsonify(UserData().dump(auth.current_user())), 200


@app.route("/user/logout", methods=['DELETE'])
@auth.login_required(role=['admin', 'customuser'])
def logout():
    if request.method == 'DELETE':
        return {
            "message": "Success"
        }, 200
    else:
        return {
            'message': "Incorrect request"
        }, 400


@errors.errorhandler(404)
def server_error(e):
    return jsonify(message="Invalid URL provided"), 404


@errors.errorhandler(500)
def server_error(e):
    return jsonify(message="Invalid data provided"), 500


@errors.app_errorhandler(marshmallow.exceptions.ValidationError)
def handle_error(error):
    response = {
        'error': {
            'code': 400,
            'message': "Your data is not valid"
        }
    }

    return jsonify(response), 400


@api_blueprint.route("/user", methods=['POST'])
def create_user():
    try:
        user_data = CreateUser().load(request.json)
        user = create(User, **user_data)
        response = make_response(jsonify(UserData().dump(user)))
        response.status_code = 200
        return response
    except marshmallow.exceptions.ValidationError as e:
        response = make_response(jsonify(message=e.args[0], status=400))
        response.status_code = 400
        return response
    except:
        response = make_response(jsonify(message='Creation Error',status=400))
        response.status_code = 400
        return response


@api_blueprint.route("/user/<int:user_id>", methods=["GET"])
@auth.login_required(role='admin')
def get_user_by_id(user_id):
    try:
        user = get_entry_by_id(User,user_id)
        return jsonify(UserData().dump(user))
    except:
        response = make_response(jsonify(message='User is not available',status=400))
        response.status_code = 400
        return response


@api_blueprint.route("/user/<int:user_id>", methods=["PUT"])
@auth.login_required()
def update_user(user_id):
    try:
        current_user = auth.current_user()
        print(user_id, current_user.id)
        if current_user.id !=int(user_id):
            return "Access denied", 403
        else:
            user_data = UpdateUser().load(request.json)
            user = get_entry_by_id(User,user_id)
            update_entry(User, user_id, **user_data)
            response = make_response(jsonify(UserData().dump(user)))
            response.status_code = 200
            return response
    except marshmallow.exceptions.ValidationError as e:
        response = make_response(jsonify(message=e.args[0], status=400))
        response.status_code = 400
        return response
    except ValueError:
        response = make_response(jsonify(message='Invalid ID',status=400))
        response.status_code = 400
        return response
    except ValueError:
        response = make_response(jsonify(message='User not found',status=404))
        response.status_code = 404
        return response
    except sqlalchemy.exc.NoResultFound:
        response = make_response(jsonify(message='Wrong email or password', status=500))
        response.status_code = 500
        return response

@api_blueprint.route("/user/adminadd/<int:user_id>", methods=["PUT"])
@auth.login_required(role='admin')
def add_admin(user_id):
    try:
        user = get_entry_by_id(User,user_id)
        if user.role == 'admin':
            response = make_response(jsonify("Customer is already admin"))
            response.status_code = 200
            return response
        update_entry_admin(User, user_id)
        user = get_entry_by_id(User, user_id)
        response = make_response(jsonify(UserData().dump(user)))
        response.status_code = 200
        return response
    except marshmallow.exceptions.ValidationError as e:
        response = make_response(jsonify(message=e.args[0], status=400))
        response.status_code = 400
        return response
    except ValueError:
        response = make_response(jsonify(message='Invalid ID',status=400))
        response.status_code = 400
        return response
    except:
        response = make_response(jsonify(message='User not found',status=404))
        response.status_code = 404
        return response


@api_blueprint.route("/user/<int:user_id>", methods=["DELETE"])
@auth.login_required()
def delete_user(user_id):
    try:
        current_user = auth.current_user()
        print(user_id, current_user.id)
        if current_user.id != int(user_id):
            return "Access denied", 403
        get_entry_by_id(User, user_id)
        delete_entry_tickets(ScheludeHasUsers, user_id)
        delete_entry(User, user_id)
        response = make_response(jsonify(message="User deleted", status=200))
        response.status_code = 200
    except sqlalchemy.exc.NoResultFound as e:
        response = make_response(jsonify(message="Invalid ID input", status=400))
        response.status_code = 400
    return response


@api_blueprint.route("/sessions", methods=["POST"])
@auth.login_required(role='admin')
def create_session():
     try:
        session_data = CreateSession().load(request.json)
        session = create(Sessions,**session_data)
        response = make_response(jsonify(SessionData().dump(session)))
        response.status_code = 200
        return response
     except marshmallow.exceptions.ValidationError as e:
         response = make_response(jsonify(message=e.args[0], status=400))
         response.status_code = 400
         return response
     except:
         response = make_response(jsonify(message='Invalid input',status=405))
         response.status_code = 405
         return response


@api_blueprint.route("/sessions", methods=["GET"])
@auth.login_required(role='admin')
def get_sessions():
    try:
        session = get_entries(Sessions)
        return jsonify(SessionData(many=True).dump(session))
    except sqlalchemy.exc.NoResultFound as e:
        response = make_response(jsonify(message="Only admins can get all sessions", status=500))
        response.status_code = 500
        return response


@api_blueprint.route("/sessions/<int:session_id>", methods=["GET"])
@auth.login_required(role='admin')
def get_session_by_id(session_id):
    try:
        session = get_entry_by_id(Sessions,session_id)
        return jsonify(SessionData().dump(session))
    except ValueError:
        response = make_response(jsonify(message='Invalid ID',status=400))
        response.status_code = 400
        return response
    except:
        response = make_response(jsonify(message='Session not found', status=404))
        response.status_code = 404
        return response


@api_blueprint.route("/sessions/<int:session_id>", methods=["DELETE"])
@auth.login_required(role='admin')
def delete_session(session_id):
    a=delete_entry(Sessions,session_id)
    if a==True:
        response = make_response(jsonify(Id_of_deleted_session=session_id, status=200))
        response.status_code = 200
        return response
    else:
        response = make_response(jsonify(message='Session not found', status=404))
        response.status_code = 404
        return response


@api_blueprint.route("/visiting", methods=["POST"])
@auth.login_required(role='admin')
def create_visiting():
    try:
        visiting_data = CreateVisiting().load(request.json)
        visiting = create(Visiting, **visiting_data)
        response = make_response(jsonify(VisitingData().dump(visiting)))
        response.status_code = 200
        return response
    except marshmallow.exceptions.ValidationError as e:
        response = make_response(jsonify(message=e.args[0], status=400))
        response.status_code = 400
        return response
    except:
        response = make_response(jsonify(message='Invalid input',status=405))
        response.status_code = 405
        return response


@api_blueprint.route("/visiting", methods=["GET"])
@auth.login_required(role='admin')
def get_visiting():
    visiting = get_entries(Visiting)
    return jsonify(VisitingData(many=True).dump(visiting))


@api_blueprint.route("/visiting/<int:vis_id>", methods=["GET"])
@auth.login_required(role='admin')
def get_visiting_by_id(vis_id):
    try:
        visiting = get_entry_by_id(Visiting, vis_id)
        return jsonify(VisitingData().dump(visiting))
    except ValueError:
        response = make_response(jsonify(message='Invalid ID',status=400))
        response.status_code = 400
        return response
    except:
        response = make_response(jsonify(message='Visiting session not found',status=404))
        response.status_code = 404
        return response


@api_blueprint.route("/visiting/<int:vis_id>", methods=["DELETE"])
@auth.login_required(role='admin')
def delete_visiting(vis_id):
    #try:
    a=delete_entry(Visiting,vis_id)
    if a==True:
        response = make_response(jsonify(ID_of_deleted_visiting=vis_id, status=200))
        response.status_code = 200
        return response
    else:
        response = make_response(jsonify(message='Visiting not found', status=404))
        response.status_code = 404
        return response

    # user buy ticket for specific Film in specific Schedule


@api_blueprint.route("/schedule_sale/<int:user_id>/<int:sch_id>/<int:film_id>", methods=["POST"])
@auth.login_required()
def bound_user(user_id, sch_id, film_id):
    current_user = auth.current_user()
    print(user_id, current_user.id)
    if current_user.id != int(user_id):
        return "Access denied", 403
    get_entry_by_two_id(ScheludeHasFilms,sch_id,film_id)
    create_entry(ScheludeHasUsers, user_id, sch_id)
    response = make_response(jsonify(message='User was added to schedule succssesfuly', status='200'))
    response.status_code = 200
    return response


@api_blueprint.route("/schedule", methods=["POST"])
@auth.login_required(role='admin')
def create_schedule():
    try:
        schedule_data = CreateSchedule().load(request.json)
        schedule = create_return(Schelude, **schedule_data)
        response = make_response(jsonify(message='Schedule was added succssesfuly', status='200'))
        response.status_code = 200
        return response
    except marshmallow.exceptions.ValidationError as e:
        response = make_response(jsonify(message=e.args[0], status=400))
        response.status_code = 400
        return response
    except:
        response = make_response(jsonify(message='Invalid input',status=405))
        response.status_code = 405
        return response


@api_blueprint.route("/schedule", methods=["GET"])
@auth.login_required()
def get_schedule():
    schedule = get_entries(Schelude)
    return jsonify(ScheduleData(many=True).dump(schedule))


@api_blueprint.route("/schedule/<int:sch_id>", methods=["GET"])
@auth.login_required()
def get_schedule_by_id(sch_id):
    try:
        schedule = get_entry_by_id(Schelude,sch_id)
        return jsonify(ScheduleData().dump(schedule))
    except ValueError:
        response = make_response(jsonify(message='Invalid ID',status=400))
        response.status_code = 400
        return response
    except:
        response = make_response(jsonify(message='Schedule not found',status=404))
        response.status_code = 404
        return response


@api_blueprint.route("/schedule/<int:sch_id>", methods=["DELETE"])
@auth.login_required(role='admin')
def delete_schedule(sch_id):
    try:
        a=delete_entry(Schelude,sch_id)
        if a:
            response = make_response(jsonify(ID_of_deleted_schedule=sch_id, status=200))
            response.status_code = 200
            return response
        else:
            response = make_response(jsonify(message='Schedule not found', status=404))
            response.status_code = 404
            return response
    except sqlalchemy.exc.IntegrityError as e:
        response = make_response(jsonify(message="Schedule has session or visiting", status=400))
        response.status_code = 400
        return response


@api_blueprint.route("/films", methods=["POST"])
@auth.login_required(role='admin')
def create_film():
    try:
        film_data = CreateFilm().load(request.json)
        film = create_return(Films, **film_data)
        response = make_response(jsonify(message="Film was added successfully", status=200))
        response.status_code = 200
        return response
    except marshmallow.exceptions.ValidationError as e:
        response = make_response(jsonify(message=e.args[0], status=400))
        response.status_code = 400
        return response
    except:
        response = make_response(jsonify(message='Invalid input',status=405))
        response.status_code = 405
        return response


@api_blueprint.route("/films/<int:film_id>", methods=["PUT"])
@auth.login_required(role='admin')
def update_film(film_id):
    try:
        film_data = UpdateFilm().load(request.json)
        film = get_entry_by_id(Films, film_id)
        update_entry(Films, film_id, **film_data)
        response = make_response(jsonify(FilmData().dump(film)))
        response.status_code = 200
        return response
    except marshmallow.exceptions.ValidationError as e:
        response = make_response(jsonify(message=e.args[0], status=400))
        response.status_code = 400
        return response
    except ValueError:
        response = make_response(jsonify(message='Invalid ID',status=400))
        response.status_code = 400
        return response
    except:
        response = make_response(jsonify(message='Film not found',status=404))
        response.status_code = 404
        return response


@api_blueprint.route("/films", methods=["GET"])
@auth.login_required()
def get_films():
    film = get_entries(Films)
    return jsonify(FilmData(many=True).dump(film))


@api_blueprint.route("/films/<int:film_id>", methods=["GET"])
@auth.login_required()
def get_film_by_id(film_id):
    try:
        film = get_entry_by_id(Films,film_id)
        return jsonify(FilmData().dump(film))
    except ValueError:
        response = make_response(jsonify(message='Invalid ID',status=400))
        response.status_code = 400
        return response
    except:
        response = make_response(jsonify(message='Film not found', status=404))
        response.status_code = 404
        return response


@api_blueprint.route("/films/<int:film_id>", methods=["DELETE"])
@auth.login_required(role='admin')
def delete_film(film_id):
    a=delete_entry(Films,film_id)
    if a:
        response = make_response(jsonify(ID_of_deleted_film=film_id,status=200))
        response.status_code = 200
        return response
    else:
        response = make_response(jsonify(message='Film not found', status=400))
        response.status_code = 400
        return response


    # connect Film to Schedule
@api_blueprint.route("/schedule_film", methods=["POST"])
@auth.login_required(role='admin')
def bound_admin():
    try:
        admin_data = CreateSheduleFilm().load(request.json)
        if get_entry_scalar(ScheludeHasFilms,**admin_data) is not None:
            response = make_response(jsonify(message='Invalid input', status=405))
            response.status_code = 405
            return response
        admin = create(ScheludeHasFilms, **admin_data)
        response = make_response(jsonify(message="Film was added to schedule successfully", status=200))
        response.status_code = 200
        return response
    except marshmallow.exceptions.ValidationError as e:
        response = make_response(jsonify(message=e.args[0], status=400))
        response.status_code = 400
        return response
    except:
        response = make_response(jsonify(message='Invalid input',status=405))
        response.status_code = 405
        return response

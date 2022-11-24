from marshmallow import validate, Schema, fields
from werkzeug.security import generate_password_hash
from datetime import date
from models import *


class UserData(Schema):
	id = fields.Integer()
	firstname = fields.String()
	lastname = fields.String()
	email = fields.String(validate=validate.Email())
	role = fields.String()


class CreateUser(Schema):
	firstname = fields.String()
	lastname = fields.String()
	email = fields.String(validate=validate.Email())
	password = fields.Function(
		deserialize=lambda obj: generate_password_hash(obj), load_only=True
	)
	role = fields.String(validate=validate.OneOf(["admin", "customuser"]))


class UpdateUser(Schema):
	firstname = fields.String()
	lastname = fields.String()
	email = fields.String(validate=validate.Email())
	password = fields.Function(
		deserialize=lambda obj: generate_password_hash(obj), load_only=True
	)
	role = fields.String(validate=validate.OneOf(["admin", "customuser"]))


class ScheduleData(Schema):
	id = fields.Integer()
	num_of_movies = fields.Integer()


class CreateSchedule(Schema):
	num_of_movies = fields.Integer()


class UpdateSchedule(Schema):
	num_of_movies = fields.Integer()


class SessionData(Schema):
	id = fields.Integer()
	sch_id = fields.Integer()  # fields.Nested(ScheduleData(only=("id",)))
	showtime = fields.Float()
	num_of_sessions = fields.Integer()


class CreateSession(Schema):
	sch_id = fields.Integer()  # fields.Nested(ScheduleData(only=("id",)))
	showtime = fields.Float()
	num_of_sessions = fields.Integer()


class UpdateSession(Schema):
	sch_id = fields.Integer()  # fields.Nested(ScheduleData(only=("id",)))
	showtime = fields.Float()
	num_of_sessions = fields.Integer()


class FilmData(Schema):
	id = fields.Integer()
	name = fields.String()
	genre = fields.String()
	duration = fields.Float()
	rating = fields.Float()
	release_date = fields.Date(validate=lambda x: x < date.today())


class CreateFilm(Schema):
	name = fields.String()
	genre = fields.String()
	duration = fields.Float()
	rating = fields.Float()
	release_date = fields.Date(validate=lambda x: x < date.today())


class UpdateFilm(Schema):
	name = fields.String()
	genre = fields.String()
	duration = fields.Float()
	rating = fields.Float()
	release_date = fields.Date(validate=lambda x: x < date.today())


class VisitingData(Schema):
	id = fields.Integer()
	sch_id = fields.Integer()  # fields.Nested(ScheduleData(only=("id",)))
	num_of_people = fields.Integer()


class CreateVisiting(Schema):
	sch_id = fields.Integer()  # fields.Nested(ScheduleData(only=("id",)))
	num_of_people = fields.Integer()


class UpdateVisiting(Schema):
	sch_id = fields.Integer()  # fields.Nested(ScheduleData(only=("id",)))
	num_of_people = fields.Integer()


class SheduleUsersData(Schema):
	schedule_id = fields.Integer()
	user_id = fields.Integer()


class CreateSheduleUsers(Schema):
	schedule_id = fields.Integer()
	user_id = fields.Integer()


class SheduleFilmData(Schema):
	schelude_id = fields.Integer()
	films_id = fields.Integer()


class CreateSheduleFilm(Schema):
	schelude_id = fields.Integer()
	films_id = fields.Integer()
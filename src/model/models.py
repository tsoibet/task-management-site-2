import enum
from datetime import datetime
from flask.json import dump
from database import db
from marshmallow import Schema, fields, post_load, validates_schema, ValidationError
from marshmallow.validate import Length, Range, OneOf
from flask_marshmallow import Marshmallow

from sqlalchemy.orm.attributes import flag_modified

class Status(enum.Enum):
    TO_DO = 1
    IN_PROGRESS = 2
    DONE = 3

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(40), nullable=False)
    detail = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum(Status), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    deadlineness = db.Column(db.Boolean, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.TIMESTAMP,  server_default = db.func.now())

    def __init__(self, title, detail, status, priority, deadlineness, deadline=None):
        self.title = title
        self.detail = detail
        self.status = status
        self.priority = priority
        self.deadlineness = deadlineness
        if deadlineness is True:
            self.deadline = deadline
        else:
            self.deadline = datetime(9999,12,31,0,0,0)

    def update_dict(self, dict):
        for name, value in dict.items():
            if name in self.__dict__ and name:
                setattr(self, name, value)
        if dict['deadlineness'] is False:
            self.deadline = datetime(9999,12,31,0,0,0)
        

ma = Marshmallow()


class TaskSchema(ma.SQLAlchemyAutoSchema):
    status = fields.Method("get_status")

    def get_status(self, obj):
        return obj.status.name
    class Meta:
        model = Task


class CreateTaskInputSchema(Schema):
    title = fields.Str(required=True, validate=Length(max=40))
    detail = fields.Str(required=True, validate=Length(max=1024))
    status = fields.Str(required=True, validate=OneOf(
        [Status.TO_DO.name, Status.IN_PROGRESS.name, Status.DONE.name]))
    priority = fields.Int(required=True, validate=Range(min=1))
    deadlineness = fields.Boolean(required=True)
    deadline = fields.DateTime()

    @validates_schema
    def validate_deadline(self, data, **kwargs):
        errors = {}
        if data["deadlineness"] is True and "deadline" not in data:
            errors["deadline"] = ["deadline is required."]
            raise ValidationError(errors)
    @post_load
    def make_task(self, data, **kwargs):
        return Task(**data)


class QueryTaskInputSchema(Schema):
    page = fields.Int(validate=Range(min=1), missing=1)
    per = fields.Int(validate=Range(min=1), missing=20)
    sort = fields.Str(missing="status")

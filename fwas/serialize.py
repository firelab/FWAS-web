from marshmallow import Schema, fields, validate
from marshmallow_sqlalchemy import ModelSchema

from .models import Alert, Notification, User


class UserSchema(ModelSchema):
    class Meta:
        model = User


class UserParameter(Schema):
    user_id = fields.Int()


class UserError(Schema):
    message = fields.String()


class NewUserParameter(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=10))
    phone = fields.String(required=True)


class LoginResult(Schema):
    status = fields.String(required=True)
    message = fields.String(required=True)
    auth_token = fields.String()


class LoginParameter(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=10))


class LoginStatusData(Schema):
    user_id = fields.String(required=True)
    email = fields.Email(required=True)
    admin = fields.Boolean(required=True)
    created_at = fields.DateTime(required=True)


class LoginStatusResult(Schema):
    status = fields.String(required=True)
    data = fields.Nested(LoginStatusData, required=True)


class AlertSchema(ModelSchema):
    class Meta:
        model = Alert
        exclude = ("geom",)


class NotificationSchema(ModelSchema):
    class Meta:
        model = Notification


user_schema = UserSchema()
alert_schema = AlertSchema()
notification_schema = NotificationSchema()

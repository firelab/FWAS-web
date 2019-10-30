from marshmallow import Schema, fields
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
    email = fields.Email()
    phone = fields.String()


class NewUserResult(Schema):
    id = fields.Int()
    uuid = fields.String()


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

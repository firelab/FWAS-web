from marshmallow import Schema, fields
from marshmallow_sqlalchemy import ModelSchema

from .models import Alert, Notification, User


class UserSchema(ModelSchema):
    class Meta:
        model = User
        exclude = ("password",)


class UserParameter(Schema):
    user_id = fields.Int()


class UserError(Schema):
    message = fields.String()


class Error(Schema):
    status = fields.String()
    message = fields.String()


class InternalError(Error):
    """Represents internal errors (i.e. HTTP 5xx)"""


class RequestError(Error):
    """Represents request errors (i.e. HTTP 4xx)"""


class AlertShareError(Error):
    """Represents errors with subscribing a user to an alert."""


class NewUserParameter(Schema):
    email = fields.Email(required=True)
    username = fields.String(required=True)
    password = fields.String(required=True)
    phone = fields.String(required=True)


class LoginResult(Schema):
    status = fields.String(required=True)
    message = fields.String(required=True)
    auth_token = fields.String()


class LoginParameter(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


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


class AlertCreationSuccess(Schema):
    status = fields.String(required=True)
    message = fields.String(required=True)
    alert_id = fields.Int(required=True)
    alert_uuid = fields.String(required=True)


class AlertShareSuccess(Schema):
    status = fields.String(required=True)
    message = fields.String(required=True)


class AlertDetailsParameters(Schema):
    since = fields.DateTime()


class NewAlertSchema(Schema):
    name = fields.String(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    radius = fields.Float(required=True)
    timezone = fields.String()

    temperature_limit = fields.Float()
    relative_humidity_limit = fields.Float()
    wind_limit = fields.Float()
    precipitation_limit = fields.Float()


class NotificationSchema(ModelSchema):
    model = Notification


user_schema = UserSchema()
alert_schema = AlertSchema()
notification_schema = NotificationSchema()
new_alert_schema = NewAlertSchema()

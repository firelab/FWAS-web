from flask_wtf import FlaskForm
from wtforms import HiddenField, PasswordField, StringField
from wtforms.validators import DataRequired, Length
from wtforms_alchemy import Unique
from wtforms_components import Email, EmailField

from ..models import User, db
from ..utils import ModelForm
from .validators import ensure_identity_exists


class LoginForm(FlaskForm):
    next = HiddenField()
    identity = StringField("Username or email", [DataRequired(), Length(3, 254)])
    password = PasswordField("Password", [DataRequired(), Length(8, 128)])


class BeginPasswordResetForm(FlaskForm):
    identity = StringField(
        "Username or email", [DataRequired(), Length(3, 254), ensure_identity_exists]
    )


class PasswordResetForm(FlaskForm):
    reset_token = HiddenField()
    password = PasswordField("Password", [DataRequired(), Length(8, 128)])


class SignupForm(ModelForm):
    email = EmailField(
        validators=[
            DataRequired(),
            Email(),
            Unique(User.email, get_session=lambda: db.session),
        ]
    )
    password = PasswordField("Password", [DataRequired(), Length(8, 128)])

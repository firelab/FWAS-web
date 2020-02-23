from datetime import datetime
from uuid import UUID

from .models import Alert, Notification, User

from pydantic import BaseModel, EmailStr


class UserInDB(BaseModel):
    class Meta:
        model = User
        exclude = ("password",)

    class Config:
        orm_mode = True


class UserRequest(BaseModel):
    user_id: int


class UserError(BaseModel):
    message: str


class UserIn(BaseModel):
    email: EmailStr
    username: str
    password: str
    phone: str


class TokenResponse(BaseModel):
    status: str
    message: str
    auth_token: Optional[str]


class LoginParameter(BaseModel):
    email: str
    password: str


class LoginStatusData(BaseModel):
    user_id: str
    email: EmailStr
    admin: bool
    created_at: datetime


class LoginStatusResult(BaseModel):
    status: str
    data: LoginStatusData


class AlertInDB(ModelBaseModel):
    Config:
        orm_mode = True


class AlertCreationSuccess(BaseModel):
    status: str
    message: str
    alert_id: int
    alert_uuid: UUID


class AlertShareSuccess(BaseModel):
    status: str
    message: str


class AlertDetailsParameters(BaseModel):
    since: datetime


class NewAlertBaseModel(BaseModel):
    name: str
    latitude: float
    longitude: float
    radius: float
    timezone: Optional[str]

    temperature_limit: Optional[float] = None
    relative_humidity_limit: Optional[float] = None
    wind_limit: Optional[float] = None
    precipitation_limit: Optional[float] = None


class NotificationBaseModel(BaseModel):
    model: Notification


class Error(BaseModel):
    status: str
    message: str


class InternalError(Error):
    """Represents internal errors (i.e. HTTP 5xx)"""


class RequestError(Error):
    """Represents request errors (i.e. HTTP 4xx)"""


class AlertShareError(Error):
    """Represents errors with subscribing a user to an alert."""

from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth
from flask_login import LoginManager

auth = HTTPBasicAuth()
bcrypt = Bcrypt()
login = LoginManager()

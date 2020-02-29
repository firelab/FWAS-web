import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
basedir = os.path.abspath(os.path.dirname(__file__))

API_PREFIX = "/api"
ALLOWED_HOSTS = "0.0.0.0"
VERSION = "0.1.0"
PROJECT_NAME = "Fire Weather Alert Service"
DEBUG = os.getenv("APP_DEBUG", True)


SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.getenv("SECRET_KEY", "catcat")
BCRYPT_LOG_ROUNDS = os.getenv("BCRYPT_LOG_ROUNDS", 12)
REMEMBER_COOKIE_DURATION = 3600

import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "catcat")
    BCRYPT_LOG_ROUNDS = os.getenv("BCRYPT_LOG_ROUNDS", 12)


class TestConfig(Config):
    DEBUG = True
    TESTING = True

    SQLALCHEMY_DATABASE_URI = "postgresql://docker:docker@localhost:5432/unittests"

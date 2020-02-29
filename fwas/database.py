from databases import Database

from fwas.config import SQLALCHEMY_DATABASE_URI

database = Database(SQLALCHEMY_DATABASE_URI)

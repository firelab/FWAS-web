from . import create_app
from .database import db

app = create_app()
db.create_all()

from .development import *

SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URI")

CALLBACK_URL = environ.get("CALLBACK_URL")

SECRET_KEY = environ.get("SECRET_KEY")

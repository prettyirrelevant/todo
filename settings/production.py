from .development import *

SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")

CALLBACK_URL = environ.get("CALLBACK_URL")

SECRET_KEY = environ.get("SECRET_KEY")

AUTH0_DOMAIN = environ.get("AUTH0_DOMAIN")

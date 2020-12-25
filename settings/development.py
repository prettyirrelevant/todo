from pathlib import Path
from os import environ

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '%f6zsA<@hcb|5JbeNGnI!/NEX}^dzGS)%?AVKBNxJ]z9&8"ta)}#ZS-dRlBexBc'

SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR}/todo.db"

SQLALCHEMY_TRACK_MODIFICATIONS = False

CLIENT_ID = environ.get("CLIENT_ID")

CLIENT_SECRET = environ.get("CLIENT_SECRET")

AUTH0_DOMAIN = "prettyirrelevant.us.auth0.com"

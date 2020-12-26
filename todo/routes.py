from urllib.parse import urlencode

from flask import current_app as app, render_template, url_for, redirect, flash
from flask_login import login_user, current_user, logout_user

from . import oauth, db
from .models import User

auth0 = oauth.register(
    "auth0",
    client_id=app.config.get("CLIENT_ID"),
    client_secret=app.config.get("CLIENT_SECRET"),
    api_base_url=app.config.get("AUTH0_DOMAIN"),
    access_token_url=f'{app.config.get("AUTH0_DOMAIN")}/oauth/token',
    authorize_url=f'{app.config.get("AUTH0_DOMAIN")}/authorize',
    client_kwargs={"scope": "openid profile email"},
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return auth0.authorize_redirect(
        redirect_uri=app.config["CALLBACK_URL"], audience=""
    )


@app.route("/callback")
def callback():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    auth0.authorize_access_token()
    resp = auth0.get("userinfo")
    userinfo = resp.json()

    # checks for existing email
    existing_user = User.query.filter_by(email=userinfo["email"]).first()
    if existing_user:
        login_user(existing_user)
        flash("logged in successfully", "success")
        return redirect(url_for("index"))

    # new registration
    new_user = User(
        name=userinfo["name"], email=userinfo["email"], picture=userinfo["picture"]
    )

    try:
        db.session.add(new_user)
        db.session.commit()
    except:
        db.session.rollback()
        flash("something went wrong", "error")
        return redirect(url_for("index"))
    else:
        login_user(new_user)
        flash("logged in successfully", "success")

    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    logout_user()
    params = {
        "returnTo": url_for("index", _external=True),
        "client_id": app.config["CLIENT_ID"],
    }
    flash('logged out successfully', 'success')
    return redirect(auth0.api_base_url + "/v2/logout?" + urlencode(params))

from urllib.parse import urlencode

from flask import current_app as app, render_template, url_for, redirect, flash, request
from flask_login import login_user, current_user, logout_user, login_required

from . import oauth, db
from .forms import AddTodoForm
from .models import User, Tag, Todo

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
    form = AddTodoForm()

    # pagination
    page = request.args.get("page", 1, type=int)
    todos = current_user.todos.order_by(Todo.created_on.desc()).paginate(page, 3, False)
    next_url = url_for("index", page=todos.next_num) if todos.has_next else None
    prev_url = url_for("index", page=todos.prev_num) if todos.has_prev else None
    return render_template(
        "index.html", form=form, todos=todos, next_url=next_url, prev_url=prev_url
    )


@app.route("/login")
def login():
    return auth0.authorize_redirect(
        redirect_uri=app.config["CALLBACK_URL"], audience=""
    )


@app.route("/delete_todo/<id>")
@login_required
def delete_todo(id):
    todo = current_user.todos.filter_by(id=id).first()
    print(todo)
    if not todo:
        flash("sorry, todo does not exist", "error")
        return redirect(url_for("index"))

    try:
        db.session.delete(todo)
        db.session.commit()
    except:
        flash("something went wrong", "error")
        return redirect(url_for("index"))

    flash("todo deleted successfully", "success")
    return redirect(url_for("index"))


@app.route("/add_todo", methods=["POST"])
@login_required
def add_todo():
    form = AddTodoForm(request.form)
    if form.validate_on_submit():
        # tag validation
        validated_tags = []
        tags = set([_.lower().strip() for _ in form.tags.data.split(",") if _ != ""])

        if len(tags) != 0:
            for tag in tags:
                __ = Tag.query.filter_by(name=tag).first()
                if __:
                    validated_tags.append(__)
                else:
                    try:
                        new_tag = Tag(name=tag)
                        db.session.add(new_tag)
                        db.session.commit()
                        validated_tags.append(new_tag)
                    except:
                        pass
        new_todo = Todo(user_id=current_user.id, text=form.text.data)
        new_todo.tags.extend(validated_tags)
        try:
            db.session.add(new_todo)
            db.session.commit()
        except:
            flash("something went wrong", "error")
            return redirect(url_for("index"))

        flash("todo added successfully", "success")
        return redirect(url_for("index"))
    return redirect(url_for("index"))


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
        name=userinfo["name"],
        email=userinfo["email"],
        picture=f"https://avatars.dicebear.com/4.5/api/human/{userinfo.get('name')}.svg",
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
@login_required
def logout():
    logout_user()
    params = {
        "returnTo": url_for("index", _external=True),
        "client_id": app.config["CLIENT_ID"],
    }
    flash("logged out successfully", "success")
    return redirect(auth0.api_base_url + "/v2/logout?" + urlencode(params))

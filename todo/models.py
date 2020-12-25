from flask_login import UserMixin
from sqlalchemy import func

from . import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


todo_tags = db.Table(
    "todo_tags",
    db.Column("todo_id", db.Integer, db.ForeignKey("todos.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    picture = db.Column(db.String(250), nullable=False)
    created_on = db.Column(db.DateTime, default=func.now())
    todos = db.relationship("Todo", backref="user", lazy="dynamic")


class Todo(db.Model):
    __tablename__ = "todos"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime, default=func.now())
    updated_on = db.Column(db.DateTime, default=func.now())
    tags = db.relationship(
        "Tag",
        secondary=todo_tags,
        backref=db.backref("todos", lazy="dynamic"),
        lazy=True,
    )


class Tag(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

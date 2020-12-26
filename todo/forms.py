from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import Length, DataRequired


class AddTodoForm(FlaskForm):
    tags = StringField("Tags", validators=[Length(max=150)])
    text = TextAreaField("Text", validators=[DataRequired(), Length(min=1)])

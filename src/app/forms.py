from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    SelectField,
    TextAreaField,
    StringField,
    BooleanField,
    PasswordField,
)
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class MessageForm(FlaskForm):
    message = TextAreaField("", validators=[Length(max=140)])
    dialect = SelectField(
        u"Product",
        choices=[("GOMA", "Goeland ou Malouine"), ("LPBF", "Lolly Pop ou Baby Flac")],
    )
    submit = SubmitField("Submit")

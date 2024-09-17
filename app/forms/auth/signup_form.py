from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Regexp

class SignupForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=8, max=20)])
    email = StringField("Email", validators=[DataRequired(), Length(min=12, max=120)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=20), Regexp(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$", message="should contains at least one lowercase letter, one uppercase letter, and one digit")])

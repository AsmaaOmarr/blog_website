from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(min=12, max=120)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=20)])

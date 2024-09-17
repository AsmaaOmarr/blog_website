from flask_wtf import FlaskForm
from wtforms import StringField, FloatField,IntegerField
from wtforms.validators import DataRequired, Length

class EditForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=2, max=20)])
    content = StringField("Content", validators=[DataRequired(), Length(min=2, max=800)])
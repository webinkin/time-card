from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SubmitField, TimeField
from wtforms.validators import DataRequired
import datetime


class TimeInput(FlaskForm):
    date = DateField("Date", default=datetime.datetime.today(), validators=[DataRequired()])
    arrived = TimeField("Arrival Time", validators=[DataRequired()])
    departed = TimeField("Departure Time", validators=[DataRequired()])
    submit = SubmitField("Submit Hours")
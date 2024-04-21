from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class AddFilms(FlaskForm):
    genre = SelectField("Жанр", choices=[('~'), ('Комедия'), ('Боевик')], validators=[DataRequired()])
    film_duration = StringField("Продолжительность", validators=[DataRequired()])
    submit = SubmitField('Применить')
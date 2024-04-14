from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class AddFilms(FlaskForm):
    film = StringField('Название фильма', validators=[DataRequired()])
    genre = StringField("Жанр", validators=[DataRequired()])
    film_duration = StringField("Продолжительность", validators=[DataRequired()])
    submit = SubmitField('Применить')
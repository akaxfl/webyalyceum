from flask_wtf import FlaskForm
from sqlalchemy_serializer import SerializerMixin
from wtforms import StringField, TextAreaField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class AddFilms(FlaskForm, SerializerMixin):
    film = StringField('Название фильма', validators=[DataRequired()])
    genre = StringField("Жанр", validators=[DataRequired()])
    film_duration = StringField("Продолжительность", validators=[DataRequired()])
    description = TextAreaField("Подробности", validators=[DataRequired()])
    submit = SubmitField('Добавить фильм')
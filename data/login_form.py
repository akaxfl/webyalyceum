from flask_wtf import FlaskForm
from sqlalchemy_serializer import SerializerMixin
from wtforms import PasswordField, BooleanField, SubmitField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm, SerializerMixin):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

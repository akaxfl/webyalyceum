import sqlite3

from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from WebProject.data.add_films import AddFilms
from data import db_session
from data.films import Films
from data.login_form import LoginForm
from data.register import RegisterForm
from data.users import User

application = Flask(__name__)
application.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(application)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@application.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        # if user and user.check_password(form.password.data):
        if user:
            login_user(user, remember=form.remember_me.data)
            return redirect('/search')
        return render_template('login.html', message='Неправильный логин или пароль', form=form)
    return render_template('login.html', title='Авторизация', form=form)


@application.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают.")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Этот пользователь уже существует.")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@application.route('/add', methods=['GET', 'POST'])
@login_required
def add_films():
    form = AddFilms()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        films = Films()
        films.film = form.film.data
        films.genre = form.genre.data
        films.film_duration = form.film_duration.data
        current_user.films.append(films)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('add_films.html', title='Добавление фильма',
                           form=form)


@application.route("/")
def base():
    return render_template("main.html")


@application.route("/recommend")
def recommendation():
    form = AddFilms()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        films = Films()
        films.genre = form.genre.data
        films.film_duration = form.film_duration.data
        current_user.films.append(films)
        db_sess.merge(current_user)
        db_sess.commit()
    return render_template("recomendation.html", form=form)


@application.route("/help")
def helping():
    return render_template("help.html")


@application.route("/search")
def search():
    session = db_session.create_session()
    films = session.query(Films).all()
    users = session.query(User).all()
    names = {name.id: (name.surname, name.name) for name in users}
    return render_template("search.html", films=films, names=names, title='Поиск')


@application.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@application.route('/add/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_films(id):
    form = AddFilms()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(Films).filter(Films.id == id,
                                           Films.user == current_user
                                           ).first()
        if news:
            form.film.data = news.film
            form.genre.data = news.genre
            form.film_duration.data = news.film_duration
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(Films).filter(Films.id == id,
                                           Films.user == current_user
                                           ).first()
        if news:
            news.film = form.film.data
            news.genre = form.genre.data
            news.film_duration = form.film_duration.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('add_films.html',
                           title='Редактирование новости',
                           form=form
                           )


@application.route('/add_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def films_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Films).filter(Films.id == id,
                                       Films.user == current_user
                                       ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


def main():
    db_session.global_init("db/webproject.sql")
    application.run()


if __name__ == '__main__':
    main()

import random
import sqlite3

import flask
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect, abort, request, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from WebProject.data.add_films import AddFilms
from data import db_session, films_api
from data.films import Films
from data.login_form import LoginForm
from data.register import RegisterForm
from data.users import User
from flask_restful import Api

application = Flask(__name__)
application.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
blueprint = flask.Blueprint('jobs_api', __name__, template_folder='templates')

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
        if user and user.check_password(form.password.data):
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
        films.description = form.description.data
        current_user.films.append(films)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/search')
    return render_template('add_films.html', title='Добавление фильма',
                           form=form)


def latest_news(channel_name):
    telegram_url = 'https://t.me/s/'
    channel_name = 'echolyceum'
    url = telegram_url + channel_name
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    link = soup.find_all('a')
    url = link[-1]['href']
    url = url.replace('https://t.me/', '')
    channel_name, news_id = url.split('/')
    urls = []
    for i in range(5):
        urls.append(f'{channel_name}/{int(news_id) - i}')
    return urls


@application.route("/")
def base():
    url = 'melfm/4960'
    channel_name = 'echolyceum'
    urls = latest_news(channel_name)
    return render_template("main.html", urls=urls)


@application.route("/recommend")
def recommendation():
    con = sqlite3.connect('db/webproject.sql')
    cur = con.cursor()
    cur.execute("SELECT id FROM films")
    results = cur.fetchall()
    con.close()
    res1 = results[0]
    res2 = results[1]
    res1 = int(''.join(map(str, res1)))
    res2 = int(''.join(map(str, res2)))
    result = random.randint(res1, res2)
    return render_template("recomendation.html", title='Рекомендации', id=result)


@application.route("/help")
def helping():
    return render_template("help.html", title='Справка')


def getfilms(search):
    con = sqlite3.connect('db/webproject.sql')
    cur = con.cursor()
    cur.execute(
        "SELECT * FROM `films` WHERE `film` LIKE ?",
        ("%" + search + "%",)
    )
    results = cur.fetchall()
    con.close()
    return results


@application.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        data = dict(request.form)
        users1 = getfilms(data["search"])
    else:
        users1 = []
    session = db_session.create_session()
    films = session.query(Films).all()
    users = session.query(User).all()
    names = {name.id: (name.surname, name.name) for name in users}
    return render_template("search.html", usr=users1, films=films, names=names, title='Поиск')


@application.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@application.route('/add_detail/<int:id>', methods=['GET', 'POST'])
def film_detail(id):
    if request.method == "GET":
        db_sess = db_session.create_session()
        films = db_sess.query(Films).filter(Films.id == id,
                                            ).first()
        users = db_sess.query(User).all()
        names = {name.id: (name.surname, name.name) for name in users}

        return render_template('description.html', title='Подробности', films=films, names=names)


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
            form.description.data = news.description
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
            news.description = form.description.data
            db_sess.commit()
            return redirect('/search')
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
    return redirect('/search')


@application.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@application.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


def main():
    db_session.global_init("db/webproject.sql")
    application.register_blueprint(films_api.blueprint)
    application.run()


if __name__ == '__main__':
    main()

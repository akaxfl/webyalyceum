import flask
from flask import jsonify, make_response, request

from . import db_session
from .films import Films

blueprint = flask.Blueprint(
    'films_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/films')
def get_news():
    db_sess = db_session.create_session()
    news = db_sess.query(Films).all()
    return jsonify(
        {
            'films':
                [item.to_dict(only=('film', 'genre', 'added_by'))
                 for item in news]
        }
    )


@blueprint.route('/api/films/<int:news_id>', methods=['GET'])
def get_one_news(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(Films).get(news_id)
    if not news:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'films': news.to_dict(only=(
                'film', 'genre', 'film_duration', 'description', 'adding_date', 'added_by'))
        }
    )


@blueprint.route('/api/films', methods=['POST'])
def create_news():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['film', 'genre', 'film_duration', 'description', 'adding_date', 'added_by']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    film = Films(
        film=request.json['film'],
        genre=request.json['genre'],
        film_duration=request.json['film_duration'],
        description=request.json['description'],
        adding_date=request.json['adding_date'],
        added_by=request.json['added_by']
    )
    db_sess.add(film)
    db_sess.commit()
    return jsonify({'id': film.id})


@blueprint.route('/api/films/<int:film_id>', methods=['DELETE'])
def delete_news(film_id):
    db_sess = db_session.create_session()
    film = db_sess.query(Films).get(film_id)
    if not film:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(film)
    db_sess.commit()
    return jsonify({'success': 'OK'})

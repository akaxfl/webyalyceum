from requests import get, post, delete

print(post('http://localhost:5000/api/films',
           json={'film': 'Крутой',
                 'genre': 'Жанр',
                 'film_duration': 120,
                 'description': 'Очень крутой',
                 'adding_date': '',
                 'added_by': '10'}).json())

print(delete('http://localhost:5000/api/films/999').json())

print(delete('http://localhost:5000/api/films/8').json())

print(post('http://localhost:5000/api/films', json={}).json())

print(post('http://localhost:5000/api/films',
           json={'film': 'Заголовок'}).json())

print(get('http://localhost:5000/api/films').json())

print(get('http://localhost:5000/api/films/3').json())

print(get('http://localhost:5000/api/films/999').json())
# фильма с id = 999 нет в базе

print(get('http://localhost:5000/api/films/q').json())



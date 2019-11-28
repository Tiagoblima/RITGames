import json
import os
from sys import intern

import requests
from collections import namedtuple
from datetime import timedelta
from functools import update_wrapper
from flask import Flask, make_response, request, current_app
from flask import flash, redirect
from flask import render_template
from past.types import basestring
from config import Config
from connection import Connection
from forms import RegistrationForm, User, LoginForm
from server import Server

app = Flask(__name__, template_folder='templates')
app.debug = 'DEBUG' in os.environ
app.config['CORS_HEADERS'] = 'Content-Type'
app.config.from_object(Config)

sender = Connection()
sender.set_dest_port(os.environ.get("PORT"))


def crossdomain(origin=None, methods=None, headers=None, max_age=21600, attach_to_all=True, automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)

    return decorator


# Standard loopback interface address (localhost)
PORT = os.environ.get("PORT")  # Port to listen on (non-privileged ports are > 1023)


def save_user(form):
    response = requests.post("https://rit-bd.herokuapp.com/conta/cadastrar/" +
                             form.first_name.data + ' ' + form.last_name.data + '/' +
                             form.username.data + '/' +
                             form.password.data + '/' +
                             form.email.data + '/' + 'user')

    print(response.status_code)

    if response.status_code is 200:
        return "Cadastro Realizado com sucesso!"
    else:
        return "Erro ao cadastrar tente novamente"


def do_login(username='', password=''):
    user = ''
    try:
        user = get_cache(username)
    except FileNotFoundError:
        response = requests.get("https://rit-bd.herokuapp.com/conta/logar/" + username + '/' + password)

        if response.status_code is 200:
            user = response.content
    try:
        return True, json.loads(user)
    except json.decoder.JSONDecodeError:
        pass

    return False, "Login ou senha incorretos"


def get_games():
    response = requests.get('https://rit-gameserver.herokuapp.com/games/')
    return json.loads(response.content)


def get_game(_id):
    response = requests.get('https://rit-gameserver.herokuapp.com/games/' + _id)
    return response


CACHE_PATH = os.path.join(os.getcwd(), 'cache/')


def get_cache(name):
    path = os.path.join(CACHE_PATH, name + '.json')
    with open(path, 'r') as file:
        return file.read()


def cache_data(name, data):
    path = os.path.join(CACHE_PATH, name + '.json')
    with open(path, 'w') as file:
        file.write(json.dumps(data))


def delete_cache():
    for item in os.listdir(CACHE_PATH):
        if intern(item) is not intern('package.json'):
            os.remove(os.path.join(CACHE_PATH, item))


def format_games(dic):
    games_dic = {}

    for game, _id in zip(dic.values(), dic.keys()):

        game['_id'] = str(_id)
        try:
            inside = False
            for row in games_dic[game['categoria']]:
                if len(row) <= 4:
                    row.append(game)
                    inside = True

            if not inside:
                games_dic[game['categoria']].append([game])

        except KeyError:
            games_dic[game['categoria']] = [[game]]

    return games_dic


def get_user(name):
    response = requests.get('https://rit-bd.herokuapp.com/conta/get-nome/' + name.replace(' ', '%20'))
    print(response.status_code)
    print(response.content)
    if response.status_code is 200:
        return json.loads(response.content)

    return {'msg': "Homepage unreachable"}


@app.route('/game_page/<_id>')
def game_page(_id):
    games_dic = get_games()
    return render_template('game_page.html', game=games_dic[str(_id)])


@app.route('/games')
def games():
    games_dic = format_games(get_games())
    return render_template('games.html', categorias=games_dic.keys(), games=games_dic,
                           row_lim=4, game_count=0)


@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/')
def run_start():
    return index()


@app.route('/index', methods=['GET', 'POST'])
def index(name=None):
    delete_cache()
    login = LoginForm(request.form)

    user = User()
    if login.is_submitted():
        print(login.username.data + '/' + login.password.data)
        data = do_login(login.username.data, login.password.data)

        if data[0]:
            cache_data(data[1]['login'], data[1])
            return redirect('/start/' + data[1]['login'])
        else:
            flash("Login ou senha incorretos")

    return render_template('index.html', login=login, dir=CACHE_PATH)


@app.route('/start/<name>', methods=['GET', 'POST'])
def start(name):
    user = json.loads(get_cache(name))
    return render_template('start.html', user=user)


@app.route('/dev/<username>')
def dev(username):
    user = json.loads(get_cache(username))
    return render_template('dev.html', user=user)


@app.route('/<name>')
def homepage(name):
    print(get_user(name))
    return render_template('homepage.html', user=get_user(name))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if form.is_submitted():
        if form.validate_on_submit():
            msg = save_user(form)
            flash(msg)
    return render_template('auth/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login = LoginForm(request.form)
    if login.is_submitted():
        result, data = do_login(username=login.username.data, password=login.password.data)
        if not result:
            flash(data)
        else:
            flash('Login realizado!')

    return render_template('auth/login.html', login=login)


if __name__ == '__main__':
    app.run(debug=True)

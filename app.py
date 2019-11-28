import json
import os

from datetime import timedelta
from functools import update_wrapper
from flask import Flask, make_response, request, current_app
from flask import flash, redirect
from flask import render_template
from past.types import basestring
from util.config import Config
from util.connection import get_games, do_login, get_user, save_user, add_game
from forms import RegistrationForm, User, LoginForm, GameForm
from util.util import format_games, delete_cache, cache_data, get_cache

app = Flask(__name__, template_folder='templates')
app.debug = 'DEBUG' in os.environ
app.config['CORS_HEADERS'] = 'Content-Type'
app.config.from_object(Config)


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
CACHE_PATH = os.path.join(os.getcwd(), 'cache/')


@app.route('/game_page/<_id>')
def game_page(_id):
    games_dic = get_games()
    return render_template('game_page.html', game=games_dic[str(_id)])


@app.route('/games')
def games():
    games_dic = format_games(get_games())
    return render_template('games.html', categorias=games_dic.keys(), games=games_dic)


@app.route('/game_form')
def game_form():
    form = GameForm(request.form)

    if form.is_submitted() and form.validate_on_submit():
        game = {
            "nome": form.name.data,
            "categoria": form.categoria.data,
            "url": form.url_game.data,
            "url_image": form.url_image.data,
            "description": form.description.data
        }
        add_game(game)
    return render_template('game_form.html', form=form)


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

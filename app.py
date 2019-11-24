import json
import os
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
    user = User(form.first_name.data + ' ' + form.last_name.data,
                form.username.data.replace('.', '_'),
                form.email.data.replace('.', '_'),
                form.password.data)
    sender.send_obj("\"" + user.to_json().replace("\'", '') + "\"")

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


def get_user(data):
    user = json.loads(data, object_hook=lambda d: namedtuple('USER', d.keys(), rename=True)(*d.values()))

    with open(user.login + '.json', 'w') as file:
        j_data = json.dumps(user, indent=4, separators=(',', ': '))
        s = json.dumps(j_data, indent=4, sort_keys=True)

        file.write(s)
    return user


def do_login(username='', password=''):
    response = requests.get("https://rit-bd.herokuapp.com/conta/logar/" + username + '/' + password)

    if response.status_code is 200:
        user = response.content
        return True, user

    return False, "Login ou senha incorretos"


@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/')
def run_start():
    return index()


@app.route('/index', methods=['GET', 'POST'])
def index(name=None):
    login = LoginForm(request.form)

    user = User()
    if login.is_submitted():
        print(login.username.data + '/' + login.password.data)
        data = do_login(login.username.data, login.password.data)

        try:
            user = get_user(data[1])
            user_json = json.dumps(user, indent=4, separators=(',', ': '))
            return start(user)
        except json.decoder.JSONDecodeError:
            flash("Login ou senha incorretos")

    return render_template('index.html', login=login)


@app.route('/start', methods=['GET', 'POST'])
def start(user):
    return render_template('start.html', user=user)


@app.route('/dev.html/<username>')
def dev(username):
    with open(username + '.json', 'r') as file:
        user = json.loads(file.read(), object_hook=lambda d: namedtuple('USER', d.keys())(*d.values()))
    print(user)
    return render_template('dev.html', user=user)


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

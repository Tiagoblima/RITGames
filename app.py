from collections import namedtuple
from datetime import timedelta
from functools import update_wrapper
from flask import Flask, url_for, flash, redirect, request
from flask import render_template
from flask import Flask, make_response, request, current_app
from past.types import basestring
from connection import Connection
from server import Server
from config import Config
from forms import Form
app = Flask(__name__, template_folder='templates')

app.config['CORS_HEADERS'] = 'Content-Type'
app.config.from_object(Config)

sender = Connection()
sender.set_dest_port(6789)

listener = Connection()


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


def save_user(form):
    flash("Cadastro Realizado com sucesso!")
    user = User(form.first_name.data + ' ' + form.last_name.data,
                form.username.data.replace('.', '_'),
                form.email.data.replace('.', '_'),
                form.password.data)

    sender.send_obj("\"" + user.to_json().replace("\'", '') + "\"")


def do_login(username=''):
    login = LoginForm(request.form)
    if login.is_submitted():
        print('Hello World')
        print(login.to_json())

        sender.send_obj(login.to_json())

    data = '{}'
    user = None
    try:
        with open(username + '.json') as file:
            data = file.read()
    except FileNotFoundError:

        data = listener.listening(6457)

        user = json.loads(data, object_hook=lambda d: namedtuple('USER', d.keys())(*d.values()))
        with open(user.username + '.json', 'w') as file:

            j_data = json.dumps(user, indent=4, separators=(',', ': '))
            s = json.dumps(j_data, indent=4, sort_keys=True)

            file.write(s)
            listener.close()

    return user


@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/')
def run_start():
    return index()


@app.route('/index.html')
def index(name=None):
    return render_template('index.html')


@app.route('/start', methods=['GET', 'POST'])
def start(username=None):
    user = do_login()
    return render_template('start.html', user=user)


@app.route('/start.html')
def start(name=None):
    return render_template('start.html', name=name)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if form.is_submitted():
        if form.validate_on_submit():
            save_user(form)
        else:
            flash("Cadastro não pôde ser realizado.")
    return render_template('auth/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    login = LoginForm(request.form)
    return render_template('auth/login.html', login=login)


if __name__ == '__main__':
    app.run(debug=True)

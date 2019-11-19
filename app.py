from collections import namedtuple
from pprint import pprint

from flask import Flask, url_for, flash, redirect, request
from flask import render_template
from config import Config
from forms import RegistrationForm, User, LoginForm
from connection import Connection
import json

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)


def save_user(form):
    flash("Cadastro Realizado com sucesso!")
    user = User(form.first_name.data + ' ' + form.last_name.data,
                form.username.data,
                form.email.data,
                form.password.data)
    sender = Connection()
    try:

        sender.set_dest_port(9000)
        sender.send_obj(user.to_json())
    finally:
        sender.close()


def do_login(username=''):
    login = LoginForm(request.form)
    if login.is_submitted():
        print('Hello World')
        print(login.to_json())
        sender_login = Connection()
        sender_login.set_dest_port(9000)
        try:
            print(login.to_json())
            sender_login.send_obj(login.to_json())
        finally:
            sender_login.close()

    try:
        with open(username + '.json') as file:
            user = json.loads(file.read(), object_hook=lambda d: namedtuple('USER', d.keys())(*d.values()))
    except FileNotFoundError:
        listener = Connection()
        data = listener.listening(6457)
        user = json.loads(data, object_hook=lambda d: namedtuple('USER', d.keys())(*d.values()))
        with open(user.username + '.json', 'w') as file:

            j_data = json.dumps(user, indent=4, separators=(',', ': '))
            s = json.dumps(j_data, indent=4, sort_keys=True)

            file.write(s)
            listener.close()

    return user


@app.route('/')
def run_start():
    return index()


@app.route('/index.html', methods=['GET', 'POST'])
def index(name=None):
    global conn
    form = RegistrationForm(request.form)
    if form.is_submitted():
        if form.validate_on_submit():
            save_user(form)
        else:
            flash("Cadastro não pôde ser realizado, verifique os campos.")

    login = LoginForm(request.form)

    form = RegistrationForm(request.form)

    return render_template('index.html', form=form, login=login)


@app.route('/start/', methods=['GET', 'POST'])
def start(username=None):
    user = do_login()
    return render_template('start.html', user=user)


@app.route('/dev.html/<username>')
def dev(username):
    with open(username + '.json', 'r') as file:
        user = json.loads(file.read(), object_hook=lambda d: namedtuple('USER', d.keys())(*d.values()))
    print(user)
    return render_template('dev.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)

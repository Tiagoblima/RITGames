from collections import namedtuple
from pprint import pprint

from flask import Flask, url_for, flash, redirect, request
from flask import render_template
from config import Config
from forms import RegistrationForm, User, LoginForm
from connection import Connection
import json

"""
  if form.is_submitted():
        if form.validate_on_submit():
            save_user(form)
        else:
            flash("Cadastro não pôde ser realizado, verifique os campos.")
"""
app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)


def save_user(form):
    flash("Cadastro Realizado com sucesso!")
    user = User(form.first_name.data + form.last_name.data,
                form.username.data,
                form.email.data,
                form.password.data)
    sender = Connection()
    try:

        sender.set_dest_port(5005)
        sender.send_obj(user.to_json())
    finally:
        sender.close()


@app.route('/')
def run_start():
    return index()


@app.route('/index.html', methods=['GET', 'POST'])
def index(name=None):
    global conn
    login = LoginForm(request.form)

    if login.is_submitted():
        print('Hello World')
        print(login.to_json())
        sender_login = Connection()
        sender_login.set_dest_port(9000)
        try:
            # print(login.to_json())
            sender_login.send_obj(login.to_json())
        finally:
            sender_login.close()
            redirect('/start.html')

    form = RegistrationForm(request.form)

    return render_template('index.html', form=form, login=login)


@app.route('/start.html', methods=['GET', 'POST'])
def start(name=None):
    user = User()
    data = user
    if data:
        data_user = data

        pprint(data_user)
    #        user = json.loads(data, object_hook=lambda d: namedtuple('USER', d.keys())(*d.values()))

    return render_template('start.html', user=user)


@app.route('/dev.html')
def dev():
    return render_template('dev.html')


if __name__ == '__main__':
    app.run(debug=True)

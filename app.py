from pprint import pprint

from flask import Flask, url_for, flash, redirect, request
from flask import render_template
from config import Config
from forms import RegistrationForm, User, LoginForm
from connection import Connection
import json

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)


@app.route('/')
def run_start():
    return index()


@app.route('/index.html', methods=['GET', 'POST'])
def index(name=None):
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        flash("Cadastro Realizado com sucesso!")
        user = User(form.first_name.data + form.last_name.data,
                    form.username.data,
                    form.email.data,
                    form.password.data)

        conn = Connection()
        conn.send_obj(user.to_json())

    if not form.validate() and form.is_submitted():
        flash("Cadastro não pôde ser realizado, verifique os campos.")

    login = LoginForm()
    return render_template('index.html', form=form, login=login)


@app.route('/start.html', methods=['GET', 'POST'])
def start(name=None):
    with open('data_user.json') as f_user:
        data_user = json.loads(f_user)

    pprint(data_user)

    user = User(data_user['name'], data_user['username'], data_user['email'], data_user['password'])

    return render_template('start.html', user=user)


@app.route('/dev.html')
def dev():
    return render_template('dev.html')


if __name__ == '__main__':
    app.run(debug=True)

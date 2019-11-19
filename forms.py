from flask import json
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class RegistrationForm(FlaskForm):
    tipo = 'registrationForm'
    first_name = StringField('inputFirstName')
    last_name = StringField('inputLastName')
    email = StringField('inputEmail', validators=[DataRequired(message='Campo Obrigatório'), Email('E-mail inválido')])

    username = StringField('Username', validators=[DataRequired(message='Campo Obrigatório')])
    password = PasswordField('inputPassword1',
                             validators=[DataRequired(message='Campo Obrigatório'),
                                         EqualTo('confirm_pass', 'As senhas devem ser iguais')])

    confirm_pass = PasswordField('inputPassword2', validators=[DataRequired(message='Campo Obrigatório')])
    agree = BooleanField('Agree')
    submit = SubmitField('Cadastrar')
    login = SubmitField('Login')


class LoginForm(FlaskForm):
    tipo = 2
    username = StringField('inputLogin', validators=[DataRequired(message='Campo Obrigatório')])
    password = PasswordField('inputPassword', validators=[DataRequired(message='Campo Obrigatório')])
    submit = SubmitField('Login')

    def to_json(self):
        str_json = '{\"type\":\"' + str(self.tipo) + '\",\"username\":\"' + self.username.data + '\",\"password\":\"' \
                   + self.password.data + '\"}'
        # str_json.replace("'", "\"")

        return str_json


class User:
    type = 1
    name = ''
    username = ''
    email = ''
    password = ''
    msg = ''
    dashboard = None

    def __init__(self, name='', username='', email='', password=''):
        self.type = 1
        self.name = name
        self.username = username
        self.email = email
        self.password = password

    def set_username(self, username):
        self.username = username

    def set_msg(self, msg):
        self.msg = msg

    def set_email(self, email):
        self.email = email

    def set_password(self, password):
        self.password = password

    def to_json(self):
        return json.dumps(self.__dict__, indent=4, separators=(',', ': '))

    def set_dashboard(self, dashboard):
        self.dashboard = dashboard

import re

from flask import json
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_validator import *
from util.util import format_games


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
    username = StringField('inputLogin', validators=[DataRequired(message='Campo Obrigatório')])
    password = PasswordField('inputPassword', validators=[DataRequired(message='Campo Obrigatório')])
    submit = SubmitField('Login')

    def to_json(self):
        str_json = '{\"login\":\"' + self.username.data + '\",\"senha\":\"' \
                   + self.password.data + '\"}'
        # str_json.replace("'", "\"")

        return str_json


from util.connection import get_games


def validate_url(form, field):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if not re.match(regex, field.data):
        raise ValidationError("URL inválido")


class GameForm(FlaskForm):
    tipo = 'gameForm'
    name = StringField('inputName',  validators=[DataRequired(message='Campo Obrigatório')])
    games = format_games(get_games())
    choices = [(category, category) for category in games.keys()]

    categoria = SelectField(u'selectFiled', choices=choices, coerce=str,  validators=[DataRequired(message='Campo Obrigatório')])

    url_game = StringField('inputUrlGame',
                           validators=[DataRequired(message='Campo Obrigatório'), validate_url])

    url_image = StringField('inputUrlImage', validators=[validate_url])

    description = TextAreaField('description')
    agree = BooleanField('Agree', validators=[DataRequired(message="Você deve concordar com os termos")])

    submit = SubmitField('Cadastrar')


class User:
    type = 1
    name = ''
    username = ''
    email = ''
    password = ''
    msg = ''
    dashboard = None

    def __init__(self, name='', username='', email='', password=''):
        self.type = "user"
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

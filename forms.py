from flask import json
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class RegistrationForm(FlaskForm):
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


class User:
    name = ''
    username = ''
    email = ''
    password = ''
    msg = ''
    dashboard = None

    def __init__(self, name='', username='', email='', password=''):
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
        with open('data_user.json', 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=4)

    def set_dashboard(self, dashboard):
        self.dashboard = dashboard

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


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

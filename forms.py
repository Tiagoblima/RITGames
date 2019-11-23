from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class Form(FlaskForm):
    first_name = StringField('inputFirstName', validators=[DataRequired()])
    last_name = StringField('inputLastName', validators=[DataRequired()])
    email = StringField('inputEmail')

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('inputPassword1', validators=[DataRequired()])
    confirm_pass = PasswordField('inputPassword2', validators=[DataRequired()])
    agree = BooleanField('Agree')
    submit = SubmitField('Sign In')

from email import message
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired(), Length(min=4, max=15, message='Login não corresponde aos criterios! Tem que ter entre 4 a 15 caracter.')])
    password = PasswordField('PassWord', validators=[DataRequired()])
    remember = BooleanField('Lembrar Me')
    submit = SubmitField('Login')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired(), Length(min=4, max=15, message='Login não corresponde aos criterios! Tem que ter entre 4 a 15 caracter.')])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember = BooleanField('Lembrar Me')
    submit = SubmitField('Login')

class CreateUserForm(FlaskForm):
    nome = StringField('Nome',  validators=[DataRequired(), Length(min=4, max=40, message='Nome não corresponde aos criterios! Tem que ter entre 4 a 40 caracter.')])
    login = StringField('Login', validators=[DataRequired(), Length(min=4, max=15, message='Login não corresponde aos criterios! Tem que ter entre 4 a 15 caracter.')])    
    password = PasswordField('Senha', validators=[DataRequired()])
    confiPassword = PasswordField('Confirme a Senha', validators=[DataRequired(), EqualTo('confiPassword')])
    submit = SubmitField('Cadastrar')

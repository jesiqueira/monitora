from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from app.models.bdMonitora import Users, Sites
from app import db


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired(), Length(
        min=4, max=15, message='Login não corresponde aos criterios! Tem que ter entre 4 a 15 caracter.')])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember = BooleanField('Lembrar Me')
    submit = SubmitField('Login')


class CreateUserForm(FlaskForm):
    nome = StringField('Nome',  validators=[DataRequired(), Length(
        min=4, max=40, message='Nome não corresponde aos criterios! Tem que ter entre 4 a 40 caracter.')])
    login = StringField('Login', validators=[DataRequired(), Length(
        min=4, max=15, message='Login não corresponde aos criterios! Tem que ter entre 4 a 15 caracter.')])
    email = StringField('Email', validators=[DataRequired(), Email(
        message='Verificar e-mail informado!')])
    adminUser = BooleanField('Administrar Acessos')
    leitura = BooleanField('Acesso a Leitura')
    escrita= BooleanField('Acesso a Escrita')
    ativo = BooleanField('Ativo')
    password = PasswordField('Senha', validators=[DataRequired(), Length(
        min=6, max=16, message='Se atentar ao criterio, senha deve ter no mínimo 6 e no máximo 16 caracter!')])
    confiPassword = PasswordField('Confirme a Senha', validators=[
                                  DataRequired(), EqualTo('password', message="As senhas não são iguais.")])
    siteSelect = SelectField('Site', choices=[])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        sites = db.session.query(Sites.nome).all()
        listaSite = []
        for site in sites:
            listaSite.append(site[0])
        self.siteSelect.choices = listaSite

    submit = SubmitField('Cadastrar')

    def validate_nome(self, nome):
        user = Users.query.filter_by(nome=nome.data).first()
        if user:
            raise ValidationError(
                'Nome já Cadastrado, escolha nome diferente!')

    def validate_login(self, login):
        user = Users.query.filter_by(login=login.data).first()
        if user:
            raise ValidationError(
                'Login já Cadastrado, escolha login diferente!')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'Email já Cadastrado, escolha email diferente!')


class UpdateUserForm(FlaskForm):
    idUsuario = HiddenField()
    idSite = HiddenField()
    nome = StringField('Nome',  validators=[DataRequired(), Length(
        min=4, max=40, message='Nome não corresponde aos criterios! Tem que ter entre 4 a 40 caracter.')])
    login = StringField('Login', validators=[DataRequired(), Length(
        min=4, max=15, message='Login não corresponde aos criterios! Tem que ter entre 4 a 15 caracter.')])
    email = StringField('Email', validators=[DataRequired(), Email(message='Verificar e-mail informado!')])
    adminUser = BooleanField('Administrar Acessos')
    leitura = BooleanField('Acesso a Leitura')
    escrita = BooleanField('Acesso a Escrita')
    ativo = BooleanField('Ativo')
    siteSelect = SelectField('Site', choices=[])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        site = Sites.query.get(self.idSite.data)
        self.siteSelect.choices = [site.nome]

    submit = SubmitField('Atualizar')


class UpdatePassWordUserForm(FlaskForm):
    id_user = HiddenField()
    idSite = HiddenField()
    password = PasswordField('Senha', validators=[DataRequired(), Length(
        min=6, max=16, message='Se atentar ao criterio, senha deve ter no mínimo 6 e no máximo 16 caracter!')])
    confiPassword = PasswordField('Confirme a Senha', validators=[
                                  DataRequired(), EqualTo('password', message="As senhas não são iguais.")])

    submit = SubmitField('Atualizar')


class SelecaoFormUser(FlaskForm):
    idSite = HiddenField()
    consulta = StringField('Digita aqui a consulta', validators=[DataRequired()])
    selection = SelectField(choices=['Nome', 'Login', 'Email'])
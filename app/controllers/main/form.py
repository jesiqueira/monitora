from tkinter.tix import Tree
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models.bdMonitora import Sites, Enderecos, PontoAtendimentos, Areas
from app import db


class localViewForm(FlaskForm):
    consulta = StringField('Consulta', validators=[DataRequired()])
    selection = SelectField(choices=['Serial', 'Patrimônio', 'Local'])

class SiteForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(
        min=5, max=30, message='Atenção a quantidade de caracter, mínimo 5, máximo: 30')])
    rua = StringField('Rua', validators=[DataRequired(), Length(
        min=10, max=40, message='Atenção a quantidade de caracter, mínimo 10, máximo: 30')])
    cep = StringField('Cep', validators=[DataRequired(), Length(
        min=8, max=8, message='Atenção a quantidade de caracter, mínimo 8, máximo: 8')])
    cidade = StringField('Cidade', validators=[DataRequired(), Length(
        min=5, max=40, message='Atenção a quantidade de caracter, mínimo 5, máximo: 30')])
    submit = SubmitField('Cadastrar')

    def validate_nome(self, nome):
        site = Sites.query.filter_by(nome=nome.data).first()
        if site:
            raise ValidationError('Nome já está cadastrado no sistema!')

    def validate_rua(self, rua):
        endereco = Enderecos.query.filter_by(rua=rua.data).first()
        if endereco:
            raise ValidationError('Rua já está cadastrado no sistema!')

    def validate_cep(self, cep):
        endereco = Enderecos.query.filter_by(cep=cep.data).first()
        if endereco:
            raise ValidationError('Cep já está cadastrado no sistema!')


class SiteUpdateForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(
        min=5, max=30, message='Atenção a quantidade de caracter, mínimo 5, máximo: 30')])
    rua = StringField('Rua', validators=[DataRequired(), Length(
        min=10, max=40, message='Atenção a quantidade de caracter, mínimo 10, máximo: 30')])
    cep = StringField('Cep', validators=[DataRequired(), Length(
        min=8, max=8, message='Atenção a quantidade de caracter, mínimo 8, máximo: 8')])
    cidade = StringField('Cidade', validators=[DataRequired(), Length(
        min=5, max=40, message='Atenção a quantidade de caracter, mínimo 5, máximo: 30')])
    submit = SubmitField('Atualizar')


class LocalAtendimento(FlaskForm):
    localPa = StringField('Local P.A', validators=[DataRequired(), Length(
        min=5, max=30, message='Campo obrigatório, mínimo 5, máximo 30 caracteres!')])
    localSelect = SelectField('Site', choices=[])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        sites = db.session.query(Sites.nome).all()
        listaSite = []
        for site in sites:
            listaSite.append(site[0])
            self.localSelect.choices = listaSite

    submit = SubmitField('Cadastrar')

    def validate_nome(self, localPa):
        local = PontoAtendimentos.query.filter_by(
            descricao=localPa.data).first()
        if local:
            raise ValidationError(
                'Ponto de Atendimento já está cadastrado no sistema!')


class UpdateLocal(FlaskForm):
    localPa = StringField('Local P.A', validators=[DataRequired(), Length(
        min=5, max=30, message='Campo obrigatório, mínimo 5, máximo 30 caracteres!')])
    localSelect = SelectField('Site', choices=[])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        sites = db.session.query(Sites.nome).all()
        listaSite = []
        for site in sites:
            listaSite.append(site[0])
            self.localSelect.choices = listaSite

    submit = SubmitField('Update')


class AreaForm(FlaskForm):
    area = StringField('Area', validators=[DataRequired(), Length(
        min=5, max=30, message='Campo obrigatório, mínimo 5, máximo 30 caracteres!')])
    localSelect = SelectField('Site', choices=[])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        sites = db.session.query(Sites.nome).all()
        listaSite = []
        for site in sites:
            listaSite.append(site[0])
            self.localSelect.choices = listaSite

    submit = SubmitField('Cadastrar')

    # def validate_localSelect(self, localSelect):
    #     # area = Areas.query.filter_by(nome=area.data).filter().first()
    #     print('Dentro do FORM AreaForm')
    #     print(f'Area: {self.area.data}, Site: {localSelect.data}')
    #     try:
    #         area = db.session.query(Areas).join(Areas.site).filter(Areas.nome == self.area.data and Sites.nome == localSelect.data).first()
    #     except Exception as e:
    #         print(f'Error: {e}')
    #     print(f'Local: {area}')
    #     if area:
    #         raise ValidationError('Área já está cadastrado no sistema!')

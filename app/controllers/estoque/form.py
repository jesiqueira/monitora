from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError


class EstoqueViewForm(FlaskForm):
    consulta = StringField('Consulta', validators=[DataRequired()])
    selection = SelectField(choices=['Serial', 'Patrimônio', 'Local'])


class EstoqueCadastroForm(FlaskForm):
    serial = StringField('Serial')
    patrimonio = StringField('Patrimônio')
    modelo = StringField('Modelo')
    processador = StringField('Processador')
    fabricante = StringField('Fabricante')
    tipo = SelectField(choices=[], validate_choice=False)

    submit = SubmitField('Cadastrar')


class EstoqueUpdateForm(FlaskForm):
    idSite = HiddenField()
    idEstoque = HiddenField()
    serial = StringField('Serial')
    patrimonio = StringField('Patrimônio')
    modelo = StringField('Modelo')
    processador = StringField('Processador')
    fabricante = StringField('Fabricante')
    tipo = SelectField(choices=[], validate_choice=False)

    submit = SubmitField('Atualizar')

class EstoqueMudarLocalForm(FlaskForm):
    serial = StringField('Serial')
    patrimonio = StringField('Patrimônio')
    modelo = StringField('Modelo')
    site = StringField('Site')
    tipo = StringField('Tipo')
    local = SelectField('Selecione para onde será movido esse equipamento/dispositivo', choices=[], validate_choice=False)
    pa = SelectField('Local Atendimento',choices=[], validate_choice=False)

    submit = SubmitField('Atualizar')

class EstoqueDeleteForm(FlaskForm):
    idSite = HiddenField()
    idEstoque = HiddenField()
    serial = StringField('Serial')
    patrimonio = StringField('Patrimônio')
    modelo = StringField('Modelo')
    processador = StringField('Processador')
    fabricante = StringField('Fabricante')
    tipo = SelectField(choices=[], validate_choice=False)

    submit = SubmitField('Remover')

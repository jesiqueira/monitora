from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models.bdMonitora import LocalPa, Computador, Site, Tipo
from app import db


class InventariosForm(FlaskForm):
    serial = StringField('Serial', validators=[DataRequired()])
    patrimonio = StringField('Patromônio', validators=[DataRequired(), Length(
        min=1, max=40, message='Campo obrigatório, mínimo 1 máximo 30 caracteres.')])
    hostname = StringField('Hostname', validators=[DataRequired(), Length(
        min=1, max=30, message='Campo Obrigatório, mínimo 1 no máximo 30 caracteres.')])
    selection = SelectField('Local', choices=[])
    tipoDispositivo = SelectField('Tipo equipamento', choices=[])
    submit = SubmitField('Cadastrar')

    def validate_serial(self, serial):
        inventario = Computador.query.filter_by(serial=serial.data).first()
        if inventario:
            raise ValidationError('Serial já cadastrado no sistema!')

    def validate_patrimonio(self, patrimonio):
        inventario = Computador.query.filter_by(
            patrimonio=patrimonio.data).first()
        if inventario:
            raise ValidationError('Patrimônio já cadastrado no sistema!')

    def validate_hostname(self, hostname):
        inventario = Computador.query.filter_by(
            hostname=hostname.data).first()
        if inventario:
            raise ValidationError('Hostname já cadastrado no sistema!')

    def validate_selection(self, selection):
        # inventario = db.session.query(Computador).join(LocalPa, Computador.idLocal == LocalPa.id).filter(LocalPa.descricaoPa == selection.data).first()
        inventario = db.session.query(Computador).join(Site, Computador.idSite== Site.id).join(LocalPa, Site.id== LocalPa.idSite).filter(LocalPa.descricaoPa == selection.data).first()
        if inventario:
            raise ValidationError(
                'Local já tem equipamento. Atualize ou remova equipamento anterior!')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        locais = db.session.query(LocalPa.descricaoPa).all()
        tipoDispositivos = db.session.query(Tipo.nome).all()
        listaLocal = []
        listatipoDispositivo = []
        for local in locais:
            listaLocal.append(local[0])
        self.selection.choices = listaLocal

        for tipo in tipoDispositivos:
            listatipoDispositivo.append(tipo[0])
        self.tipoDispositivo.choices = listatipoDispositivo


class UpdateInventariosForm(FlaskForm):
    idHidden = HiddenField()
    serial = StringField('Serial', validators=[DataRequired()])
    patrimonio = StringField('Patromônio', validators=[DataRequired(), Length(
        min=1, max=40, message='Campo obrigatório, mínimo 1 máximo 30 caracteres.')])
    hostname = StringField('Hostname', validators=[DataRequired(), Length(
        min=1, max=30, message='Campo Obrigatório, mínimo 1 no máximo 30 caracteres.')])
    # selection = SelectField('Local', choices=[] )
    selection = StringField('Local')
    tipoDispositivo = SelectField('Tipo equipamento', choices=[])
    submit = SubmitField('Atualizar')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        tipoDispositivos = db.session.query(Tipo.nome).all()
        listatipoDispositivo = []

        for tipo in tipoDispositivos:
            listatipoDispositivo.append(tipo[0])
        self.tipoDispositivo.choices = listatipoDispositivo


class TipoInventarioForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(
        min=1, max=40, message='Campo Obrigatório, mínimo 1 máximo de 40 caracteres.')])
    submit = SubmitField('Cadastrar')

    def validate_nome(self, nome):
        tipoInventario = Tipo.query.filter_by(nome=nome.data).first()
        if tipoInventario:
            raise ValidationError('Esse equipamento já está cadastrado!')

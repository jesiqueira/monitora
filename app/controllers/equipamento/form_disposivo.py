from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models.bdMonitora import PontoAtendimentos, DispositivosEquipamentos, TipoEquipamentos, Computadores, Areas, Sites
from app import db
from sqlalchemy import and_


class InventarioForm(FlaskForm):
    consulta = StringField('Consulta', validators=[DataRequired()])
    selection = SelectField(choices=['Serial', 'Patrimônio', 'Local'])


class InventariosNovoForm(FlaskForm):
    idSite = HiddenField()
    serial = StringField('Serial', validators=[DataRequired()])
    modelo = StringField('Modelo', validators=[DataRequired()])
    fabricante = StringField('Fabricante', validators=[DataRequired()])
    processador = StringField('Processador', validators=[DataRequired()])
    patrimonio = StringField('Patromônio', validators=[DataRequired(), Length(
        min=1, max=40, message='Campo obrigatório, mínimo 1 máximo 30 caracteres.')])
    hostname = StringField('Hostname', validators=[DataRequired(), Length(
        min=1, max=30, message='Campo Obrigatório, mínimo 1 no máximo 30 caracteres.')])
    pa = SelectField('Ponto de Atendimento', choices=[])
    tipoDispositivo = SelectField('Tipo equipamento', choices=[])
    submit = SubmitField('Cadastrar')

    def validate_serial(self, serial):
        inventario = DispositivosEquipamentos.query.filter_by(
            serial=serial.data).first()
        if inventario:
            raise ValidationError('Serial já cadastrado no sistema!')

    def validate_patrimonio(self, patrimonio):
        inventario = DispositivosEquipamentos.query.filter_by(
            patrimonio=patrimonio.data).first()
        if inventario:
            raise ValidationError('Patrimônio já cadastrado no sistema!')

    def validate_hostname(self, hostname):
        inventario = DispositivosEquipamentos.query.filter_by(
            hostname=hostname.data).first()
        if inventario:
            raise ValidationError('Hostname já cadastrado no sistema!')

    def validate_pa(self, pa):
        inventario = db.session.query(DispositivosEquipamentos.serial, PontoAtendimentos.descricao, Areas.nome).join(Computadores, DispositivosEquipamentos.id == Computadores.idDispositosEquipamento).join(
            PontoAtendimentos, Computadores.idPontoAtendimento == PontoAtendimentos.id).join(Areas, DispositivosEquipamentos.idArea == Areas.id).filter(and_(DispositivosEquipamentos.idSite == self.idSite.data, PontoAtendimentos.descricao == pa.data)).first()
        if inventario:
            raise ValidationError('Local já tem equipamento. Atualize ou remova equipamento anterior!')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.pa.data:
            locais = db.session.query(PontoAtendimentos.descricao).join(
                Sites, PontoAtendimentos.idSite == Sites.id).filter(Sites.id == self.idSite.data).all()
        else:
            locais = db.session.query(PontoAtendimentos.descricao).all()
            
        if self.idSite.data:
            tipoDispositivos = db.session.query(TipoEquipamentos.nome).join(TipoEquipamentos.site).filter(Sites.id == self.idSite.data).all()
        else:
            tipoDispositivos = db.session.query(TipoEquipamentos.nome).all()
        listaLocal = []
        listatipoDispositivo = []
        for local in locais:
            listaLocal.append(local[0])
        self.pa.choices = listaLocal

        for tipo in tipoDispositivos:
            listatipoDispositivo.append(tipo[0])
        self.tipoDispositivo.choices = listatipoDispositivo


class UpdateInventariosForm(FlaskForm):
    idDispositivo = HiddenField()
    idSite = HiddenField()
    serial = StringField('Serial')
    patrimonio = StringField('Patromônio')
    hostname = StringField('Hostname')
    selection = StringField('Ponto de Atendimento')
    tipoDispositivo = StringField('Tipo equipamento')
    submit = SubmitField('Atualizar')


class TipoInventarioForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(
        min=2, max=40, message='Campo Obrigatório, mínimo 2 máximo de 40 caracteres.')])
    site = SelectField('Site', choices=[], validate_choice=False)

    submit = SubmitField('Cadastrar')

class MudarLayoutForm(FlaskForm):
    idSite = HiddenField()
    idDispositivo = HiddenField()
    serial = StringField('Serial')
    patrimonio = StringField('Patrimônio')
    modelo = StringField('Modelo')
    tipo = StringField('Tipo')
    local = StringField('Local')
    de = StringField('Mover de:')
    para = StringField('Mover para:')
    submit = SubmitField('Realizar Mudança')

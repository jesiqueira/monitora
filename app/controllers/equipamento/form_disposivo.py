
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models.bdMonitora import Local, Dispositivo
from app import db


class Dispositivo(FlaskForm):
    serial = StringField('Serial')
    patrimonio = StringField('Patromônio', validators=[DataRequired(), Length(min=1, max=40, message='Campo obrigatório, mínimo 1 máximo ')])
    hostname = StringField('Hostname', validators=[DataRequired()])
    selection = SelectField('Local', choices=[])
    tipoDispositivo = RadioField('Tipo equipamento', choices=[
                                 ('Desktop'), ('Notebook'), ('VDI')])
    submit = SubmitField('Cadastrar')

    def validate_serial(self, serial):
        dispositivo = Dispositivo.query.filter_by(siteNome=serial.data).first()
        if dispositivo:
            raise ValidationError('Serial já cadastrado no sistema!')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        locais = db.session.query(Local.localizadoEm).all()
        listaLocal = []
        for local in locais:
            listaLocal.append(local[0])
            self.selection.choices = listaLocal

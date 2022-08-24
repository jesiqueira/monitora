from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired, length

class Equipamento(FlaskForm):
  serial = StringField('Serial', validators=[DataRequired()])
  patrimonio = StringField('Patromônio', validators=[DataRequired()])
  hostname = StringField('Hostname', validators=[DataRequired()])
  selection = SelectField('Local', choices=[('TA-BA-F1-P1'), ('TA-BB-F1-P2'), ('TB-BB-F1-P3')])
  tipoDispositivo = RadioField('Tipo equipamento', choices=[('Desktop'), ('Notebook'), ('VDI')])
  submit = SubmitField('Cadastrar')
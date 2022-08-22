from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired, length

class Equipamento(FlaskForm):
  serial = StringField('Serial', validators=[DataRequired()])
  patrimonio = StringField('Patromônio', validators=[DataRequired()])
  hostname = StringField('Hostname', validators=[DataRequired()])
  selection = SelectField('Local', choices=[('TA-BA-F1'), ('TA-BB-F1'), ('TB-BB-F1')])
  posicao = StringField('Posição', validators=[DataRequired()])
  tipoDispositivo = RadioField('Tipo equipamento', choices=[('Desktop'), ('Notebook'), ('VDI')])
  submit = SubmitField('Cadastrar')
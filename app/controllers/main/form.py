from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class EnderecoForm(FlaskForm):
  rua = StringField('Rua', validators=[DataRequired()])
  cep = StringField('Cep', validators=[DataRequired()])
  cidade = StringField('Cidade', validators=[DataRequired()])
  submit = SubmitField('Cadastrar')

class SiteForm(FlaskForm):
  nome = StringField('Nome', validators=[DataRequired()])
  submit = SubmitField('Cadastrar')
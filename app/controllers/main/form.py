from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models.bdMonitora import Site, Endereco


class SiteForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=5, max=30, message='Atenção a quantidade de caracter, mínimo 5, máximo: 30')])
    rua = StringField('Rua', validators=[DataRequired(), Length(min=10, max=40, message='Atenção a quantidade de caracter, mínimo 10, máximo: 30')])
    cep = StringField('Cep', validators=[DataRequired(), Length(min=8, max=8, message='Atenção a quantidade de caracter, mínimo 8, máximo: 8')])
    cidade = StringField('Cidade', validators=[DataRequired(), Length(min=5, max=40, message='Atenção a quantidade de caracter, mínimo 5, máximo: 30')])
    submit = SubmitField('Cadastrar')

    def validate_nome(self, nome):
      site = Site.query.filter_by(siteNome=nome.data).first()
      if site:
        raise ValidationError('Nome já está cadastrado no sistema!')
    
    def validate_rua(self, rua):
      endereco = Endereco.query.filter_by(rua=rua.data).first()
      if endereco:
        raise ValidationError('Rua já está cadastrado no sistema!')
    
    def validate_cep(self, cep):
      endereco = Endereco.query.filter_by(cep=cep.data).first()
      if endereco:
        raise ValidationError('Cep já está cadastrado no sistema!')

class localAtendimento(FlaskForm):
  nomeLocal = StringField('Local', validators=[DataRequired(), Length(min=5, max=30, message='Campo obrigatório, mínimo 5, máximo 30 caracteres!')])
  
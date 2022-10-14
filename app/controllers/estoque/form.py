from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError


class EstoqueViewForm(FlaskForm):
    consulta = StringField('Consulta', validators=[DataRequired()])
    selection = SelectField(choices=['Serial', 'Patrimônio', 'Local'])

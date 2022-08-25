from flask import render_template, Blueprint, flash, redirect, url_for
from flask_login import login_required
from app.controllers.equipamento.form_disposivo import Dispositivo

equipamento = Blueprint('equipamento', __name__)


equipamentos = [
    {
        'id': 1,
        'serial': 'XPTO0121',
        'patrimonio': 'MGS000001232',
        'hostname': 'PBR001150-M1232',
        'local': 'Predio A - Térreo',
        'posicao': 'A54',
        'tipo': 'Desktop'
    },
    {
        'id': 2,
        'serial': 'XPTO01324',
        'patrimonio': 'MGS000001243',
        'hostname': 'PBR001150-M1243',
        'local': 'Predio A - Térreo',
        'posicao': 'A53',
        'tipo': 'VDI'
    },
    {
        'id': 3,
        'serial': 'XPTO01432',
        'patrimonio': 'MGS000001432',
        'hostname': 'PBR001150-M1432',
        'local': 'Predio A - Térreo',
        'posicao': 'A52',
        'tipo': 'Desktop'
    },
    {
        'id': 4,
        'serial': 'XPTO0121',
        'patrimonio': 'MGS000001232',
        'hostname': 'PBR001150-M1232',
        'local': 'Predio A - Térreo',
        'posicao': 'A54',
        'tipo': 'Desktop'
    },
    {
        'id': 5,
        'serial': 'XPTO01324',
        'patrimonio': 'MGS000001243',
        'hostname': 'PBR001150-M1243',
        'local': 'Predio A - Térreo',
        'posicao': 'A53',
        'tipo': 'VDI'
    },
    {
        'id': 6,
        'serial': 'XPTO01432',
        'patrimonio': 'MGS000001432',
        'hostname': 'PBR001150-M1432',
        'local': 'Predio A - Térreo',
        'posicao': 'A52',
        'tipo': 'Desktop'
    },
    {
        'id': 7,
        'serial': 'XPTO0121',
        'patrimonio': 'MGS000001232',
        'hostname': 'PBR001150-M1232',
        'local': 'Predio A - Térreo',
        'posicao': 'A54',
        'tipo': 'Desktop'
    },
    {
        'id': 8,
        'serial': 'XPTO01324',
        'patrimonio': 'MGS000001243',
        'hostname': 'PBR001150-M1243',
        'local': 'Predio A - Térreo',
        'posicao': 'A53',
        'tipo': 'VDI'
    },
    {
        'id': 9,
        'serial': 'XPTO01432',
        'patrimonio': 'MGS000001432',
        'hostname': 'PBR001150-M1432',
        'local': 'Predio A - Térreo',
        'posicao': 'A52',
        'tipo': 'Desktop'
    },
    {
        'id': 10,
        'serial': 'XPTO0121',
        'patrimonio': 'MGS000001232',
        'hostname': 'PBR001150-M1232',
        'local': 'Predio A - Térreo',
        'posicao': 'A54',
        'tipo': 'Desktop'
    },
    {
        'id': 11,
        'serial': 'XPTO01324',
        'patrimonio': 'MGS000001243',
        'hostname': 'PBR001150-M1243',
        'local': 'Predio A - Térreo',
        'posicao': 'A53',
        'tipo': 'VDI'
    },
    {
        'id': 12,
        'serial': 'XPTO01432',
        'patrimonio': 'MGS000001432',
        'hostname': 'PBR001150-M1432',
        'local': 'Predio A - Térreo',
        'posicao': 'A52',
        'tipo': 'Desktop'
    }

]


@equipamento.route('/listagem')
@login_required
def listagem():
    return render_template('listagem.html', title='Listagem', equipamentos=equipamentos)


@equipamento.route('/dispotivo/novo', methods=['GET', 'POST'])
@login_required
def novo_equipamento():
    form = Dispositivo()
    if form.validate_on_submit():
        flash('Equipamento cadastrado com sucesso.', 'success')
        return redirect(url_for('equipamento.listagem'))
    return render_template('create_equipamento.html', title='Novo Equipamento', form=form)


# @disposito.route('/listagem/<int:equipamento_id>/editar')
# @login_required
# def editar(equipamento_id):
#     equipamento =

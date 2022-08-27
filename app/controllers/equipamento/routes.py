from distutils.log import ERROR
from flask import render_template, Blueprint, flash, redirect, url_for
from flask_login import login_required
from app.controllers.equipamento.form_disposivo import DispositivosForm, TipoDispositivoForm
from app.models.bdMonitora import Local, Tipo, Dispositivo, Site
from app import db

equipamento = Blueprint('equipamento', __name__)


@equipamento.route('/listagem')
@login_required
def listagem():
    try:
        equipamentos = db.session.query(Dispositivo.id, Dispositivo.serial, Dispositivo.patrimonio, Dispositivo.hostname, Local.localizadoEm, Tipo.tipoNome).join(Local, Local.id == Dispositivo.idLocal).join(Tipo, Tipo.id == Dispositivo.idTipo).all()
    except:
        print(F"Erro!")
    return render_template('listagem.html', title='Listagem', equipamentos=equipamentos)


@equipamento.route('/dispotivo/novo', methods=['GET', 'POST'])
@login_required
def novo_equipamento():
    form = DispositivosForm()
    if form.validate_on_submit():
        try:
            local = Local.query.filter_by(localizadoEm=form.selection.data).first()
        except:
            print('Erro ao Obter Local!')        
        try:
            tipo = Tipo.query.filter_by(tipoNome=form.tipoDispositivo.data).first()
        except:
            print("Erro ao obter Tipo!")
        if local and tipo:
            dispositivo = Dispositivo(serial=form.serial.data, patrimonio=form.patrimonio.data, hostanme=form.hostname.data, idLocal=local.id, idTipo=tipo.id)
            db.session.add(dispositivo)
            db.session.commit()
            flash('Equipamento cadastrado com sucesso.', 'success')
            return redirect(url_for('equipamento.listagem'))

    return render_template('create_equipamento.html', title='Novo Equipamento', form=form)

@equipamento.route('/equipamento/view')
def viewEqupamento():
    tipoEquipamentos = Tipo.query.all()
    return render_template('lista_tipoEquipamento.html', title='View Equipamento', tipoEquipamentos=tipoEquipamentos)

@equipamento.route('/equipamento/novo', methods=['GET', 'POST'])
def criarEqupamento():
    form = TipoDispositivoForm()

    if form.validate_on_submit():
        tipo = Tipo(form.nome.data)
        db.session.add(tipo)
        db.session.commit()
        flash('Equipamento cadastrado com sucesso.', 'success')
        return redirect(url_for('equipamento.viewEqupamento'))

    return render_template('create_tipoEquipamento.html', title='Cadastrar Novo Equipamento', form=form)


# @disposito.route('/listagem/<int:equipamento_id>/editar')
# @login_required
# def editar(equipamento_id):
#     equipamento =

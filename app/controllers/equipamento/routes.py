from flask import render_template, Blueprint, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user
from app.controllers.equipamento.form_disposivo import DispositivosForm, TipoDispositivoForm
from app.models.bdMonitora import Local, Tipo, Dispositivo, Site
from app import db

equipamento = Blueprint('equipamento', __name__)


@equipamento.route('/listagem')
@login_required
def listagem():
    if current_user.admin:
        try:
            equipamentos = db.session.query(Dispositivo.id, Dispositivo.serial, Dispositivo.patrimonio, Dispositivo.hostname, Local.localizadoEm, Tipo.tipoNome).join(Local, Local.id == Dispositivo.idLocal).join(Tipo, Tipo.id == Dispositivo.idTipo).all()
        except Exception as e:
            print(f"Erro! {e}")
        return render_template('equipamentos/listagem.html', title='Listagem', equipamentos=equipamentos)
    else:
        abort(403)


@equipamento.route('/dispotivo/novo', methods=['GET', 'POST'])
@login_required
def novo_equipamento():
    if current_user.admin:
        form = DispositivosForm()
        if form.validate_on_submit():
            try:
                local = Local.query.filter_by(localizadoEm=form.selection.data).first()
            except Exception as e:
                print(f'Erro ao Obter Local! {e}')        
            try:
                tipo = Tipo.query.filter_by(tipoNome=form.tipoDispositivo.data).first()
            except Exception as e:
                print(f"Erro ao obter Tipo! {e}")
            if local and tipo:
                dispositivo = Dispositivo(serial=form.serial.data, patrimonio=form.patrimonio.data, hostanme=form.hostname.data, idLocal=local.id, idTipo=tipo.id)
                db.session.add(dispositivo)
                db.session.commit()
                flash('Equipamento cadastrado com sucesso.', 'success')
                return redirect(url_for('equipamento.listagem'))

        return render_template('equipamentos/create_equipamento.html', title='Novo Equipamento', form=form)
    else:
        abort(403)

@equipamento.route('/equipamento/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editarEquipamento(id):
    if current_user.admin:
        form = DispositivosForm()
        equipamentos = db.session.query(Dispositivo.id, Dispositivo.serial, Dispositivo.patrimonio, Dispositivo.hostname, Local.localizadoEm, Tipo.tipoNome).join(Local, Local.id == Dispositivo.idLocal).join(Tipo, Tipo.id == Dispositivo.idTipo).filter(Dispositivo.id == id).first()
        
        if form.validate_on_submit():
            flash('Cadastro atualizado com sucesso', 'success')
            return redirect(url_for('equipamento.viewEqupamento'))
        
        elif request.method == 'GET':
            form.serial.data = equipamentos.serial
            form.patrimonio.data = equipamentos.patrimonio
            form.hostname.data = equipamentos.hostname
            form.selection.data = equipamentos.localizadoEm
            form.tipoDispositivo.data = equipamentos.tipoNome

        return render_template('equipamentos/update_equipamento.html', title='Editar Equipamento', legenda = 'Editar equipamento site', form=form)
    else:
        abort(403)
    

@equipamento.route('/equipamento/view')
def viewEqupamento():
    if current_user.admin:
        tipoEquipamentos = Tipo.query.all()
        return render_template('equipamentos/lista_tipoEquipamento.html', title='View Equipamento', tipoEquipamentos=tipoEquipamentos)
    else:
        abort(403)

@equipamento.route('/equipamento/novo', methods=['GET', 'POST'])
def criarEqupamento():
    if current_user.admin:
        form = TipoDispositivoForm()
        if form.validate_on_submit():
            tipo = Tipo(form.nome.data)
            db.session.add(tipo)
            db.session.commit()
            flash('Equipamento cadastrado com sucesso.', 'success')
            return redirect(url_for('equipamento.viewEqupamento'))

        return render_template('equipamentos/create_tipoEquipamento.html', title='Cadastrar Novo Equipamento', form=form)
    else:
        abort(403)


# @disposito.route('/listagem/<int:equipamento_id>/editar')
# @login_required
# def editar(equipamento_id):
#     equipamento =

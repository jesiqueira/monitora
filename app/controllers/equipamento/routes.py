from flask import render_template, Blueprint, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user
from app.controllers.equipamento.form_disposivo import InventariosForm, TipoInventarioForm, UpdateInventariosForm
from app.models.bdMonitora import Local, Tipo, Inventario, Site
from app import db
from sqlalchemy import exc

equipamento = Blueprint('equipamento', __name__)


@equipamento.route('/inventario')
@login_required
def inventario():
    if current_user.admin and current_user.ativo:
        try:
            inventarios = db.session.query(Inventario.id, Inventario.serial, Inventario.patrimonio, Inventario.hostname, Local.localizadoEm, Tipo.tipoNome).join(Local, Local.id == Inventario.idLocal).join(Tipo, Tipo.id == Inventario.idTipo).all()
        except Exception as e:
            print(f"Erro! {e}")
        return render_template('equipamentos/inventario.html', title='Inventário', equipamentos=inventarios)
    else:
        abort(403)


@equipamento.route('/dispotivo/novo', methods=['GET', 'POST'])
@login_required
def novo_equipamento():
    if current_user.admin and current_user.ativo:
        form = InventariosForm()
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
                inventario = Inventario(serial=form.serial.data, patrimonio=form.patrimonio.data, hostanme=form.hostname.data, idLocal=local.id, idTipo=tipo.id)
                db.session.add(inventario)
                db.session.commit()
                flash('Equipamento cadastrado com sucesso.', 'success')
                return redirect(url_for('equipamento.inventario'))

        return render_template('equipamentos/create_equipamento.html', title='Novo Equipamento', form=form)
    else:
        abort(403)

@equipamento.route('/atualizarInventario', methods=['POST'])
@login_required
def atualizarInventario():
    if current_user.admin and current_user.ativo:
        form = UpdateInventariosForm() 
        
        if request.method == 'POST' and request.form.get('id_inventario'):
            form.idHidden.data = request.form.get('id_inventario')
            inventarios = db.session.query(Inventario.id, Inventario.serial, Inventario.patrimonio, Inventario.hostname, Local.localizadoEm, Tipo.tipoNome).join(Local, Local.id == Inventario.idLocal).join(Tipo, Tipo.id == Inventario.idTipo).filter(Inventario.id == form.idHidden.data).first()
            form.serial.data = inventarios.serial
            form.patrimonio.data = inventarios.patrimonio
            form.hostname.data = inventarios.hostname
            form.selection.data = inventarios.localizadoEm
            form.tipoDispositivo.data = inventarios.tipoNome
            return render_template('equipamentos/update_equipamento.html', title='Editar Equipamento', legenda = 'Editar equipamento site', form=form)

        if form.validate_on_submit():
            try:
                inventario = Inventario.query.get_or_404(form.idHidden.data)
                tipo = Tipo.query.get_or_404(inventario.idTipo)                
                inventario.serial = form.serial.data
                inventario.patrimonio = form.patrimonio.data
                inventario.hostname = form.hostname.data
                tipo.tipoNome = form.tipoDispositivo.data

                db.session.commit()
                flash('Dados atualizado com sucesso', 'success')
                return redirect(url_for('equipamento.inventario'))
            except exc.IntegrityError as e:
                print(f'Error: {e}')
                flash('Local já cadastrado! Verificar dados inseridos.', 'danger')
                db.session.flush()
                db.session.rollback()
                abort(404)
        return render_template('equipamentos/update_equipamento.html', title='Editar Equipamento', legenda = 'Editar equipamento site', form=form)
        
    else:
        abort(403)
    

@equipamento.route('/equipamento/view')
def viewEqupamento():
    if current_user.admin and current_user.ativo:
        tipoEquipamentos = Tipo.query.all()
        return render_template('equipamentos/lista_tipoEquipamento.html', title='View Equipamento', tipoEquipamentos=tipoEquipamentos)
    else:
        abort(403)

@equipamento.route('/equipamento/novo', methods=['GET', 'POST'])
def criarEqupamento():
    if current_user.admin and current_user.ativo:
        form = TipoInventarioForm()
        if form.validate_on_submit():
            tipo = Tipo(form.nome.data)
            db.session.add(tipo)
            db.session.commit()
            flash('Equipamento cadastrado com sucesso.', 'success')
            return redirect(url_for('equipamento.viewEqupamento'))

        return render_template('equipamentos/create_tipoEquipamento.html', title='Cadastrar Novo Equipamento', form=form)
    else:
        abort(403)


# @disposito.route('/inventario/<int:equipamento_id>/editar')
# @login_required
# def editar(equipamento_id):
#     equipamento =

from flask import render_template, Blueprint, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user
from app.controllers.equipamento.form_disposivo import InventariosForm, TipoInventarioForm, UpdateInventariosForm
from app.models.bdMonitora import LocalPa, Tipo, Computador, Site, Status
from app import db
from sqlalchemy import exc
from datetime import date, datetime
from pytz import timezone

equipamento = Blueprint('equipamento', __name__)


@equipamento.route('/inventario')
@login_required
def inventario():
    if current_user.admin and current_user.ativo:
        try:
            # SELECT Computador.hostname, Tipo.nome, LocalPa.descricaoPa From tipoComputador JOIN Tipo on Tipo.id = tipoComputador.idTipo Join Computador, LocalPa on Computador.idLocalPa = LocalPa.id
            # inventarios = db.session.query(Computador.id, Computador.serial, Computador.hostname, Computador.patrimonio, LocalPa.descricaoPa, Tipo.nome).join(
            #     Computador, LocalPa.idSite == Computador.idSite).join(Computador.tipo, ).all()
            inventarios = db.session.query(Computador.id, Computador.serial, Computador.hostname, Computador.patrimonio, LocalPa.descricaoPa, Tipo.nome).join(Computador.tipo).filter(Computador.idLocalPa == LocalPa.id).all()
            # print(f'Aqui: {inventarios}')

        except Exception as e:
            # print(f"Erro! {e}")
            pass
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
                local = LocalPa.query.filter_by(descricaoPa=form.selection.data).first()
                site = Site.query.filter_by(id = local.idSite).first_or_404()
                data_e_hora_atuais = datetime.now()
                fuso_horario = timezone('America/Sao_Paulo')
                data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
                status = Status(1, data_e_hora_sao_paulo)
                db.session.add(status)
                db.session.commit()
                # db.session.flush()
            except Exception as e:
                print(f'Error: {e}')

            try:
                computador = Computador(serial=form.serial.data, hostname=form.hostname.data, patrimonio=form.patrimonio.data, idSite=site.id, idStatus=status.id, idlocalPa=local.id)
                tipo = Tipo.query.filter_by(nome=form.tipoDispositivo.data).first_or_404()
                computador.tipo.append(tipo)
                db.session.add(computador)
                print(computador)
                print(computador.tipo)
                db.session.commit()
                flash('Computador cadastrado com sucesso.', 'success')
                return redirect(url_for('equipamento.inventario'))
            except Exception as e:
                print(f'Erro ao Obter Pa! {e}')
                db.session.flush()
                db.session.rollback()

        return render_template('equipamentos/create_equipamento.html', title='Novo Computador', form=form)
    else:
        abort(403)


@equipamento.route('/atualizarInventario', methods=['POST'])
@login_required
def atualizarInventario():
    if current_user.admin and current_user.ativo:
        form = UpdateInventariosForm()

        if request.method == 'POST' and request.form.get('id_inventario'):
            form.idHidden.data = request.form.get('id_inventario')
            inventarios = db.session.query(Computador.id, Computador.serial, Computador.hostname, Computador.patrimonio, LocalPa.descricaoPa, Tipo.nome).join(Computador.tipo).join(LocalPa, LocalPa.id == Computador.id).filter(Computador.id == form.idHidden.data).first_or_404()
            form.serial.data = inventarios.serial
            form.patrimonio.data = inventarios.patrimonio
            form.hostname.data = inventarios.hostname
            form.selection.data = inventarios.descricaoPa
            form.tipoDispositivo.data = inventarios.nome
            return render_template('equipamentos/update_equipamento.html', title='Editar Equipamento', legenda='Editar equipamento site', form=form)

        if form.validate_on_submit():
            try:
                inventario = db.session.query(Computador).filter_by(id = form.idHidden.data).filter(Computador.tipo).first_or_404()
                tipo = Tipo.query.filter_by(nome=form.tipoDispositivo.data).first_or_404()
                inventario.serial = form.serial.data
                inventario.patrimonio = form.patrimonio.data
                inventario.hostname = form.hostname.data
                inventario.tipo = [tipo]
                db.session.commit()
                flash('Dados atualizado com sucesso', 'success')
                return redirect(url_for('equipamento.inventario'))
            except exc.IntegrityError as e:
                # print(f'Error: {e}')
                flash('Local já cadastrado! Verificar dados inseridos.', 'danger')
                db.session.flush()
                db.session.rollback()
                abort(404)
        return render_template('equipamentos/update_equipamento.html', title='Editar Equipamento', legenda='Editar equipamento site', form=form)

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

from flask import render_template, Blueprint, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user
from app.controllers.equipamento.form_disposivo import InventariosNovoForm, TipoInventarioForm, UpdateInventariosForm, InventarioForm
from app.controllers.equipamento.monitora import Monitora
from app.models.bdMonitora import LocalPa, Tipo, Computador, Site, Status
from app import db
from sqlalchemy import exc
from datetime import datetime
from pytz import timezone

equipamento = Blueprint('equipamento', __name__)


@equipamento.route('/inventario', methods=['GET', 'POST'])
@login_required
def inventario():
    if current_user.admin and current_user.ativo:
        form = InventarioForm()
        if request.method == 'POST':
            consult = '%'+form.consulta.data+'%'
            if form.selection.data == 'Serial':
                try:
                    inventarios = []
                    invent = db.session.query(Computador.id, Computador.serial, Computador.hostname, Computador.patrimonio, LocalPa.descricaoPa, Tipo.nome).join(
                        Computador, LocalPa.id == Computador.idLocalPa).join(Computador.tipo).filter(Computador.serial.like(consult)).first_or_404()
                    inventarios.append(invent)
                    if not invent:
                        flash(
                            'Verifique dados informados, nada foi localizado!', 'danger')
                    form.consulta.data = ''
                except Exception as e:
                    print(f'Erro! {e}')
            elif form.selection.data == 'Patrimônio':
                try:
                    inventarios = []
                    invent = db.session.query(Computador.id, Computador.serial, Computador.hostname, Computador.patrimonio, LocalPa.descricaoPa, Tipo.nome).join(
                        Computador, LocalPa.id == Computador.idLocalPa).join(Computador.tipo).filter(Computador.patrimonio.like(consult)).first_or_404()
                    inventarios.append(invent)
                    if not invent:
                        flash(
                            'Verifique dados informados, nada foi localizado!', 'danger')
                        try:
                            inventarios = db.session.query(Computador.id, Computador.serial, Computador.hostname, Computador.patrimonio, LocalPa.descricaoPa, Tipo.nome).join(
                                Computador.tipo).filter(Computador.idLocalPa == LocalPa.id).order_by(Computador.id).all()
                        except Exception as e:
                            # print(f"Erro! {e}")
                            pass
                        form.consulta.data = ''

                except Exception as e:
                    print(f'Erro! {e}')
            elif form.selection.data == 'Local':
                try:
                    inventarios = []
                    invent = db.session.query(Computador.id, Computador.serial, Computador.hostname, Computador.patrimonio, LocalPa.descricaoPa, Tipo.nome).join(
                        Computador, LocalPa.id == Computador.idLocalPa).join(Computador.tipo).filter(LocalPa.descricaoPa.like(consult)).first_or_404()
                    inventarios.append(invent)
                    if not invent:
                        flash(
                            'Verifique dados informados, nada foi localizado!', 'danger')
                        try:
                            inventarios = db.session.query(Computador.id, Computador.serial, Computador.hostname, Computador.patrimonio, LocalPa.descricaoPa, Tipo.nome).join(
                                Computador.tipo).filter(Computador.idLocalPa == LocalPa.id).order_by(Computador.id).all()
                        except Exception as e:
                            # print(f"Erro! {e}")
                            pass
                        form.consulta.data = ''
                except Exception as e:
                    print(f'Erro! {e}')

        elif request.method == 'GET':
            try:
                inventarios = db.session.query(Computador.id, Computador.serial, Computador.hostname, Computador.patrimonio, LocalPa.descricaoPa, Tipo.nome).join(
                    Computador.tipo).filter(Computador.idLocalPa == LocalPa.id).order_by(Computador.id).all()
            except Exception as e:
                # print(f"Erro! {e}")
                pass
        return render_template('equipamentos/inventario.html', title='Inventário', equipamentos=inventarios, form=form)
    else:
        abort(403)


@equipamento.route('/dispotivo/novo', methods=['GET', 'POST'])
@login_required
def novo_equipamento():
    if current_user.admin and current_user.ativo:
        form = InventariosNovoForm()
        if form.validate_on_submit():
            try:
                local = LocalPa.query.filter_by(
                    descricaoPa=form.selection.data).first()
                site = Site.query.filter_by(id=local.idSite).first_or_404()
                data_e_hora_atuais = datetime.now()
                fuso_horario = timezone('America/Sao_Paulo')
                data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(
                    fuso_horario)
                status = Status(1, data_e_hora_sao_paulo)
                db.session.add(status)
                db.session.commit()
            except Exception as e:
                db.session.flush()
                db.session.rollback()
                # print(f'Error: {e}')

            try:
                computador = Computador(serial=form.serial.data, hostname=form.hostname.data,
                                        patrimonio=form.patrimonio.data, idSite=site.id, idStatus=status.id, idlocalPa=local.id)
                tipo = Tipo.query.filter_by(
                    nome=form.tipoDispositivo.data).first_or_404()
                computador.tipo.append(tipo)
                db.session.add(computador)
                # print(computador)
                # print(computador.tipo)
                db.session.commit()
                flash('Computador cadastrado com sucesso.', 'success')
                return redirect(url_for('equipamento.inventario'))
            except Exception as e:
                # print(f'Erro ao Obter Pa! {e}')
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
            inventarios = db.session.query(Computador.id, Computador.serial, Computador.hostname, Computador.patrimonio, LocalPa.descricaoPa, Tipo.nome).join(
                Computador.tipo).join(LocalPa, LocalPa.id == Computador.id).filter(Computador.id == form.idHidden.data).first_or_404()
            form.serial.data = inventarios.serial
            form.patrimonio.data = inventarios.patrimonio
            form.hostname.data = inventarios.hostname
            form.selection.data = inventarios.descricaoPa
            form.tipoDispositivo.data = inventarios.nome
            return render_template('equipamentos/update_equipamento.html', title='Editar Equipamento', legenda='Editar equipamento site', form=form)

        if form.validate_on_submit():
            try:
                inventario = db.session.query(Computador).filter_by(
                    id=form.idHidden.data).filter(Computador.tipo).first_or_404()
                tipo = Tipo.query.filter_by(
                    nome=form.tipoDispositivo.data).first_or_404()
                inventario.serial = form.serial.data
                inventario.patrimonio = form.patrimonio.data
                inventario.hostname = form.hostname.data
                inventario.tipo = [tipo]
                db.session.commit()
                flash('Dados atualizado com sucesso', 'success')
                return redirect(url_for('equipamento.inventario'))
            except exc.IntegrityError as e:
                # print(f'Error: {e}')
                flash('Verificar dados inseridos!', 'danger')
                db.session.flush()
                db.session.rollback()
                # abort(404)
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

@equipamento.route('/detalhe/<tipo_relatorio>', methods=['GET'])
@login_required
def detalhe(tipo_relatorio):
    if current_user.admin and current_user.ativo:
        monitora = Monitora()
        if tipo_relatorio == 'Conectado':
            computadores = db.session.query(Computador.id, Computador.serial, Computador.hostname, Computador.patrimonio, Status.ativo, LocalPa.descricaoPa).join(
                Computador, Status.id == Computador.idStatus).join(LocalPa, Computador.idLocalPa == LocalPa.id).filter(Status.ativo == True).all()
        elif tipo_relatorio == 'Desconectado':
            computadores = monitora.statusDesconectado()
        else:
            computadores = monitora.statusAtencao()

        return render_template('equipamentos/detalhe.html', title='Informações - Dispositivos', legenda=f'{tipo_relatorio}', computadores=computadores)
    else:
        abort(403)

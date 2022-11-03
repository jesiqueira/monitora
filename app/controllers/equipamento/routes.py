from flask import render_template, Blueprint, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user
from app.controllers.equipamento.form_disposivo import InventariosNovoForm, TipoInventarioForm, UpdateInventariosForm, InventarioForm, MudarLayoutForm
from app.controllers.equipamento.monitora import Monitora
from app.models.bdMonitora import Areas, Computadores, PontoAtendimentos, TipoEquipamentos, DispositivosEquipamentos, Sites, Status
from app import db
from sqlalchemy import exc, and_
from datetime import datetime
from pytz import timezone

equipamento = Blueprint('equipamento', __name__)


@equipamento.route('/inventarios/view')
@login_required
def inventarioView():
    if (current_user.permissoes[0].leitura or current_user.permissoes[0].escrita) and current_user.ativo:
        form = InventarioForm()
        db.session.flush()
        try:
            # inventarios = db.session.query(Sites.id, Sites.nome).join(DispositivosEquipamentos, Sites.id==DispositivosEquipamentos.idSite).join(Areas, DispositivosEquipamentos.idArea==Areas.id).filter(Areas.nome=='Inventario').distinct(Sites.id).all()
            sites = db.session.query(Sites).all()
            # print(inventarios)
        except Exception as e:
            print(f'Error: {e}')
        return render_template('equipamentos/inventario_view.html', title='Inventários', legenda='Inventários cadastrados', descricao='Relação de todos os Inventarios no Sistema', sites=sites, form=form)
    else:
        abort(403)


@equipamento.route('/inventario/<int:idSite>/consulta')
@login_required
def consultaInventario(idSite):
    if (current_user.permissoes[0].leitura or current_user.permissoes[0].escrita) and current_user.ativo:
        form = InventarioForm()
        site = Sites.query.get(idSite)
        try:
            db.session.flush()
            computadores = db.session.query(DispositivosEquipamentos.id, DispositivosEquipamentos.serial, DispositivosEquipamentos.patrimonio, DispositivosEquipamentos.hostname, TipoEquipamentos.nome, PontoAtendimentos.descricao, Sites.nome.label('site')).join(
                Sites, DispositivosEquipamentos.idSite == Sites.id).join(TipoEquipamentos, DispositivosEquipamentos.idTipo == TipoEquipamentos.id).join(Areas, DispositivosEquipamentos.idArea == Areas.id).join(Computadores, DispositivosEquipamentos.id == Computadores.idDispositosEquipamento).join(PontoAtendimentos, Computadores.idPontoAtendimento == PontoAtendimentos.id).filter(and_(DispositivosEquipamentos.idSite == idSite, Areas.nome == 'Inventario')).all()
        except Exception as e:
            print(f'Error: {e}')
        if computadores:
            return render_template('equipamentos/inventario.html', title='Inventários', legenda='Dispositivos cadastrados', descricao=f'{computadores[0].site} - Relação de todos os dispositivos cadastrados no Inventário', computadores=computadores, form=form, idSite=idSite)
        else:
            return render_template('equipamentos/inventario.html', title='Inventários', legenda='Dispositivos cadastrados', descricao=f'{site.nome} - Relação de todos os dispositivos cadastrados no Inventário', computadores=computadores, form=form, idSite=idSite)
    else:
        abort(403)


@equipamento.route('/inventario', methods=['GET', 'POST'])
@login_required
def inventario():
    if (current_user.permissoes[0].leitura or current_user.permissoes[0].escrita) and current_user.ativo:
        form = InventarioForm()
        if request.method == 'POST':
            consult = '%'+form.consulta.data+'%'
            if form.selection.data == 'Serial':
                try:
                    inventarios = []
                    invent = db.session.query(DispositivosEquipamentos.id, DispositivosEquipamentos.serial, DispositivosEquipamentos.hostname, DispositivosEquipamentos.patrimonio, PontoAtendimentos.descricaoPa, TipoEquipamentos.nome).join(
                        DispositivosEquipamentos, PontoAtendimentos.id == DispositivosEquipamentos.idLocalPa).join(DispositivosEquipamentos.tipo).filter(DispositivosEquipamentos.serial.like(consult)).first_or_404()
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
                    invent = db.session.query(DispositivosEquipamentos.id, DispositivosEquipamentos.serial, DispositivosEquipamentos.hostname, DispositivosEquipamentos.patrimonio, PontoAtendimentos.descricaoPa, TipoEquipamentos.nome).join(
                        DispositivosEquipamentos, PontoAtendimentos.id == DispositivosEquipamentos.idLocalPa).join(DispositivosEquipamentos.tipo).filter(DispositivosEquipamentos.patrimonio.like(consult)).first_or_404()
                    inventarios.append(invent)
                    if not invent:
                        flash(
                            'Verifique dados informados, nada foi localizado!', 'danger')
                        try:
                            inventarios = db.session.query(DispositivosEquipamentos.id, DispositivosEquipamentos.serial, DispositivosEquipamentos.hostname, DispositivosEquipamentos.patrimonio, PontoAtendimentos.descricaoPa, TipoEquipamentos.nome).join(
                                DispositivosEquipamentos.tipo).filter(DispositivosEquipamentos.idLocalPa == PontoAtendimentos.id).order_by(DispositivosEquipamentos.id).all()
                        except Exception as e:
                            # print(f"Erro! {e}")
                            pass
                        form.consulta.data = ''

                except Exception as e:
                    print(f'Erro! {e}')
            elif form.selection.data == 'Local':
                try:
                    inventarios = []
                    invent = db.session.query(DispositivosEquipamentos.id, DispositivosEquipamentos.serial, DispositivosEquipamentos.hostname, DispositivosEquipamentos.patrimonio, PontoAtendimentos.descricaoPa, TipoEquipamentos.nome).join(
                        DispositivosEquipamentos, PontoAtendimentos.id == DispositivosEquipamentos.idLocalPa).join(DispositivosEquipamentos.tipo).filter(PontoAtendimentos.descricaoPa.like(consult)).first_or_404()
                    inventarios.append(invent)
                    if not invent:
                        flash(
                            'Verifique dados informados, nada foi localizado!', 'danger')
                        try:
                            inventarios = db.session.query(DispositivosEquipamentos.id, DispositivosEquipamentos.serial, DispositivosEquipamentos.hostname, DispositivosEquipamentos.patrimonio, PontoAtendimentos.descricaoPa, TipoEquipamentos.nome).join(
                                DispositivosEquipamentos.tipo).filter(DispositivosEquipamentos.idLocalPa == PontoAtendimentos.id).order_by(DispositivosEquipamentos.id).all()
                        except Exception as e:
                            # print(f"Erro! {e}")
                            pass
                        form.consulta.data = ''
                except Exception as e:
                    print(f'Erro! {e}')

        elif request.method == 'GET':
            try:
                # inventarios = db.session.query(DispositivosEquipamentos.id, DispositivosEquipamentos.serial, DispositivosEquipamentos.hostname, DispositivosEquipamentos.patrimonio, PontoAtendimentos.descricaoPa, Tipos.nome).join(
                #     DispositivosEquipamentos.tipo).filter(DispositivosEquipamentos.idLocalPa == PontoAtendimentos.id).order_by(DispositivosEquipamentos.id).all()
                inventarios = []
            except Exception as e:
                # print(f"Erro! {e}")
                pass
        return render_template('equipamentos/inventario.html', title='Inventário', equipamentos=inventarios, form=form)
    else:
        abort(403)


@equipamento.route('/dispotivo/<int:idSite>/novo', methods=['GET', 'POST'])
@login_required
def novo_equipamento(idSite):
    if (current_user.permissoes[0].leitura or current_user.permissoes[0].escrita) and current_user.ativo:
        form = InventariosNovoForm()
        try:
            site = Sites.query.get(idSite)
        except Exception as e:
            db.session.flush()
            print(f'Error: {e}')
        if form.validate_on_submit():
            try:
                area = db.session.query(Areas).join(Areas.site).filter(
                    and_(Sites.id == form.idSite.data, Areas.nome == 'Inventario')).first()
                tipoDispositivo = db.session.query(TipoEquipamentos).join(TipoEquipamentos.site).filter(
                    and_(Sites.id == form.idSite.data, TipoEquipamentos.nome == form.tipoDispositivo.data)).first()
                equipamento = DispositivosEquipamentos(serial=form.serial.data.upper(), hostname=form.hostname.data.upper(), patrimonio=form.patrimonio.data.upper(), modelo=form.modelo.data.upper(
                ), processador=form.processador.data.upper(), fabricante=form.fabricante.data.upper(), idArea=area.id, idSite=int(form.idSite.data), idTipo=tipoDispositivo.id)
                db.session.add(equipamento)
                db.session.commit()
            except Exception as e:
                print(f'Error: {e}')
                db.session.flush()
                db.session.rollback()

            if equipamento:
                try:
                    pa = db.session.query(PontoAtendimentos).filter(and_(
                        PontoAtendimentos.descricao == form.pa.data, PontoAtendimentos.idSite == int(form.idSite.data))).first()

                    data_e_hora_atuais = datetime.now()
                    fuso_horario = timezone('America/Sao_Paulo')
                    data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(
                        fuso_horario)

                    status = Status(ativo=True, dataHora=data_e_hora_sao_paulo)
                    db.session.add(status)
                    db.session.commit()

                    computador = Computadores(
                        idDispositosEquipamento=equipamento.id, idPontoAtendimento=pa.id, idStatus=status.id)
                    db.session.add(computador)
                    db.session.commit()

                    flash('Computador cadastro no inventário com sucesso!', 'success')
                    return redirect(url_for('equipamento.consultaInventario', idSite=idSite))
                except Exception as e:
                    print(f'Error cadastrar equipamento: {e}')
                    db.session.flush()
                    db.session.rollback()
            else:
                flash('Falha ao realizar cadastro computador no inventário.', 'danger')
                return redirect(url_for('equipamento.consultaInventario', idSite=idSite))

        elif request.method == 'GET':
            try:
                pontoAtendimentos = db.session.query(PontoAtendimentos.descricao).join(
                    Sites, PontoAtendimentos.idSite == Sites.id).filter(Sites.id == idSite).all()
            except Exception as e:
                print(f'Error: {e}')

            try:
                tiposEquipamentos = db.session.query(TipoEquipamentos.nome).join(
                    TipoEquipamentos.site).filter(Sites.id == idSite).all()
            except Exception as e:
                db.session.flush()
                print(f'Error: {e}')

            # form.selection.choices = [ponto.descricao for ponto in pontoAtendimentos]
            form.idSite.data = idSite
            form.pa.choices = list(
                map(lambda ponto: ponto.descricao, pontoAtendimentos))
            form.tipoDispositivo.choices = list(
                map(lambda tipo: tipo.nome, tiposEquipamentos))
            return render_template('equipamentos/create_equipamento.html', title='Novo Computador', form=form, legenda='Cadastrar novo dispositivo', idSite=idSite, descricao=f'Cadastrar novo Computador no site: {site.nome}')
        else:
            return render_template('equipamentos/create_equipamento.html', title='Novo Computador', form=form, legenda='Cadastrar novo dispositivo', idSite=idSite, descricao=f'Cadastrar novo Computador no site: {site.nome}')
    else:
        abort(403)


@equipamento.route('/atualizarInventario', methods=['POST'])
@login_required
def atualizarInventario():
    if (current_user.permissoes[0].leitura or current_user.permissoes[0].escrita) and current_user.ativo:
        form = UpdateInventariosForm()

        if form.validate_on_submit():
            try:
                computador = db.session.query(DispositivosEquipamentos).filter_by(id=int(form.idDispositivo.data)).first_or_404()
                computador.serial = form.serial.data.upper()
                computador.patrimonio = form.patrimonio.data.upper()
                computador.hostname = form.hostname.data.upper()
                db.session.commit()
                flash('Dados atualizado com sucesso', 'success')
                return redirect(url_for('equipamento.consultaInventario', idSite=form.idSite.data))
            except exc.IntegrityError as e:
                # print(f'Error: {e}')
                flash('Verificar dados inseridos!', 'danger')
                db.session.flush()
                db.session.rollback()
                # abort(404)
            return render_template('equipamentos/update_equipamento.html', title='Editar Equipamento', legenda='Editar equipamento site', form=form)

        elif request.method == 'POST' and request.form.get('idDispositivo') and request.form.get('idSite'):
            form.idDispositivo.data = request.form.get('idDispositivo')
            form.idSite.data = request.form.get('idSite')
            inventarios = db.session.query(DispositivosEquipamentos.id, DispositivosEquipamentos.serial, DispositivosEquipamentos.hostname, DispositivosEquipamentos.patrimonio,
                                           PontoAtendimentos.descricao, TipoEquipamentos.nome).join(DispositivosEquipamentos, TipoEquipamentos.id == DispositivosEquipamentos.idTipo).join(Areas, DispositivosEquipamentos.idArea == Areas.id).join(Computadores, DispositivosEquipamentos.id == Computadores.idDispositosEquipamento).join(PontoAtendimentos, Computadores.idPontoAtendimento == PontoAtendimentos.id).filter(and_(DispositivosEquipamentos.idSite==int(form.idSite.data), Areas.nome=='Inventario', DispositivosEquipamentos.id==int(form.idDispositivo.data))).first()
            form.serial.data = inventarios.serial
            form.patrimonio.data = inventarios.patrimonio
            form.hostname.data = inventarios.hostname
            form.selection.data = inventarios.descricao
            form.tipoDispositivo.data = inventarios.nome
            return render_template('equipamentos/update_equipamento.html', title='Editar Equipamento', legenda='Editar equipamento site', form=form)

    else:
        abort(403)


@equipamento.route('/moverEstoque', methods=['POST'])
@login_required
def inventarioMoverEstoque():
    if (current_user.permissoes[0].leitura or current_user.permissoes[0].escrita) and current_user.ativo:
        if request.method == 'POST' and request.form.get('idDispositivo') and request.form.get('idSite'):
            try:
                computador = db.session.query(Computadores).join(DispositivosEquipamentos, DispositivosEquipamentos.id == Computadores.idDispositosEquipamento).filter(and_(
                    Computadores.idDispositosEquipamento == int(request.form.get('idDispositivo')), DispositivosEquipamentos.idSite == int(request.form.get('idSite')))).first()
                db.session.delete(computador)
                db.session.commit()
            except Exception as e:
                # print(f'Error: {e}')
                db.session.flush()
                db.session.rollback()
                flash('Erro ao remover computador do Site.', 'danger')
                return redirect(url_for('equipamento.consultaInventario', idSite=request.form.get('idSite')))

            if computador:
                try:
                    area = db.session.query(Areas).join(DispositivosEquipamentos, Areas.id == DispositivosEquipamentos.idArea).filter(
                        and_(DispositivosEquipamentos.idSite == int(request.form.get('idSite')), Areas.nome=='Estoque')).first()
                    dispositivo = db.session.query(DispositivosEquipamentos).filter(
                        and_(DispositivosEquipamentos.id == int(request.form.get('idDispositivo')), DispositivosEquipamentos.idSite == int(request.form.get('idSite')))).first()
                    dispositivo.idArea = area.id
                    db.session.commit()

                    flash('Movido para estoque com sucesso!', 'success')
                    return redirect(url_for('equipamento.consultaInventario', idSite=request.form.get('idSite')))
                except Exception as e:
                    # print(f'Error: {e}')
                    db.session.flush()
                    db.session.rollback()
                    flash('Erro ao mover computador para estoque.', 'danger')
                    return redirect(url_for('equipamento.consultaInventario', idSite=request.form.get('idSite')))
            else:
                flash('Erro ao remover computador do Site.', 'danger')
                return redirect(url_for('equipamento.consultaInventario', idSite=request.form.get('idSite')))

        else:
            flash('Erro ao tentar mover para estoque!', 'success')
            return redirect(url_for('equipamento.consultaInventario', idSite=1))
    else:
        abort(403)

@equipamento.route('/equipamento/view')
@login_required
def equipamentoView():
    if (current_user.permissoes[0].leitura or current_user.permissoes[0].escrita) and current_user.ativo:
        form = InventarioForm()
        try:
            sites = db.session.query(Sites).all()
        except Exception as e:
            print(f'Error: {e}')
        return render_template('equipamentos/tipo_view.html', title='Equipamentos', legenda='Tipo Dispositivos/equipamento', descricao='Selecione o Site para acessar.', form=form, sites=sites)
    else:
        abort(403)


@equipamento.route('/equipamento/<int:idSite>/consulta')
@login_required
def equipamentoConsulta(idSite):
    if (current_user.permissoes[0].leitura or current_user.permissoes[0].escrita) and current_user.ativo:
        try:
            # tipoEquipamentos = TipoEquipamentos.query.all()
            try:
                tipoEquipamentos = db.session.query(TipoEquipamentos.id, TipoEquipamentos.nome, Sites.nome.label(
                    'site')).join(TipoEquipamentos.site).filter(Sites.id == idSite).all()
                return render_template('equipamentos/lista_tipoEquipamento.html', title='View Equipamento', legenda='Tipos Dispositos/Equipamentos', descricao=f'Relação de todos tipos dispositivos/equipamentos cadastrado para: {tipoEquipamentos[0].site}.', tipoEquipamentos=tipoEquipamentos, idSite=idSite)
            except TypeError as t:
                print(f'Tipo de erro: {t}')
        except Exception as e:
            print(f'Erro ao realizar consulta: {e}')
        return render_template('equipamentos/lista_tipoEquipamento.html', title='View Equipamento', legenda='Tipos Dispositos/Equipamentos', descricao='Relação de todos tipos dispositivos/equipamentos cadastrado no site', tipoEquipamentos=tipoEquipamentos, idSite=idSite)
    else:
        abort(403)


@equipamento.route('/equipamento/<int:idSite>/novo', methods=['GET', 'POST'])
@login_required
def criarEquipamento(idSite):
    if (current_user.permissoes[0].leitura or current_user.permissoes[0].escrita) and current_user.ativo:
        form = TipoInventarioForm()
        try:
            site = Sites.query.get(idSite)
        except Exception as e:
            print(f'Erro: {e}')
        if form.validate_on_submit():
            equipamento = db.session.query(TipoEquipamentos).join(TipoEquipamentos.site).filter(
                and_(TipoEquipamentos.nome == form.nome.data, Sites.id == idSite)).first()
            if not equipamento:
                tipo = TipoEquipamentos(
                    nome=form.nome.data.title(), site=[site])
                db.session.add(tipo)
                db.session.commit()
                flash('Equipamento cadastrado com sucesso.', 'success')
                return redirect(url_for('equipamento.equipamentoConsulta', idSite=idSite))
            else:
                flash(
                    f'Dispositivo/Equipamento: {form.nome.data}, já está cadastrado!', 'danger')
                return redirect(url_for('equipamento.criarEquipamento', idSite=idSite))
        else:
            form.site.choices = [site.nome]
            return render_template('equipamentos/create_tipoEquipamento.html', title='Cadastrar Novo Equipamento', legenda='Cadastrar Tipo Equipamento', descricao='Preenchar todos os campos para cadastrar novo tipo.', form=form)
    else:
        abort(403)


@equipamento.route('/inventarioMoverDescarte', methods=['POST'])
@login_required
def inventarioMoverDescarte():
    if (current_user.permissoes[0].leitura or current_user.permissoes[0].escrita) and current_user.ativo:
        if request.method == 'POST' and request.form.get('idDispositivo') and request.form.get('idSite'):
            try:
                computador = db.session.query(Computadores).join(DispositivosEquipamentos, DispositivosEquipamentos.id == Computadores.idDispositosEquipamento).filter(and_(
                    Computadores.idDispositosEquipamento == int(request.form.get('idDispositivo')), DispositivosEquipamentos.idSite == int(request.form.get('idSite')))).first()
                db.session.delete(computador)
                db.session.commit()
            except Exception as e:
                # print(f'Error: {e}')
                db.session.flush()
                db.session.rollback()
                flash('Erro ao remover computador do Site.', 'danger')
                return redirect(url_for('equipamento.consultaInventario', idSite=request.form.get('idSite')))
            
            if computador:
                try:
                    area = db.session.query(Areas).join(Areas.site).filter(and_(Sites.id == int(request.form.get('idSite')), Areas.nome == 'Descarte')).first()
                    dispositivo = db.session.query(DispositivosEquipamentos).filter(
                        and_(DispositivosEquipamentos.id == int(request.form.get('idDispositivo')), DispositivosEquipamentos.idSite == int(request.form.get('idSite')))).first()
                    dispositivo.idArea = area.id
                    db.session.commit()
                    flash('Movido para Descarte com sucesso!', 'success')
                    return redirect(url_for('equipamento.consultaInventario', idSite=request.form.get('idSite')))
                except Exception as e:
                    # print(f'Error: {e}')
                    db.session.flush()
                    db.session.rollback()
                    flash('Erro ao mover computador para Descarte.', 'danger')
                    return redirect(url_for('equipamento.consultaInventario', idSite=request.form.get('idSite')))
            else:
                flash('Erro ao remover computador do Site.', 'danger')
                return redirect(url_for('equipamento.consultaInventario', idSite=request.form.get('idSite')))
    else:
        abort(403)

@equipamento.route('/mudancaDeLayout', methods=['GET','POST'])
@login_required
def mudancaDeLayout():
    if (current_user.permissoes[0].leitura or current_user.permissoes[0].escrita) and current_user.ativo:
        form = MudarLayoutForm()
        
        if form.validate_on_submit():
            pa = db.session.query(PontoAtendimentos).filter(and_(PontoAtendimentos.idSite==int(form.idSite.data), PontoAtendimentos.descricao==form.para.data.upper())).first()
            if not pa:
                dispositivo = db.session.query(DispositivosEquipamentos.id, DispositivosEquipamentos.serial, DispositivosEquipamentos.patrimonio, DispositivosEquipamentos.modelo, Sites.nome.label('site'), TipoEquipamentos.nome.label('tipo'), PontoAtendimentos.descricao).join(DispositivosEquipamentos, TipoEquipamentos.id == DispositivosEquipamentos.idTipo).join(
                    Computadores, DispositivosEquipamentos.id == Computadores.idDispositosEquipamento).join(PontoAtendimentos, Computadores.idPontoAtendimento == PontoAtendimentos.id).filter(
                    and_(DispositivosEquipamentos.idSite == int(form.idSite.data), DispositivosEquipamentos.id == int(form.idDispositivo.data))).first()
                form.idSite.data = request.form.get('idSite')
                form.idDispositivo.data = request.form.get('idDispositivo')
                form.serial.data = dispositivo.serial
                form.patrimonio.data = dispositivo.patrimonio
                form.modelo.data = dispositivo.modelo
                form.tipo.data = dispositivo.tipo
                form.de.data = dispositivo.descricao
                flash('Local informado não existe!', 'danger')
                return render_template('equipamentos/mudar_Layout.html', title='Mudar Layout', legenda='Mudança de Layout', descricao='Informe para onde será movido o computador.', form=form, idSite=form.idSite.data)
            else:
                dispositivo = db.session.query(DispositivosEquipamentos.serial, PontoAtendimentos.descricao).join(DispositivosEquipamentos, Computadores.idDispositosEquipamento==DispositivosEquipamentos.id).join(Computadores, PontoAtendimentos.id==Computadores.idPontoAtendimento).filter(
                    and_(DispositivosEquipamentos.idSite==int(form.idSite.data), PontoAtendimentos.descricao==form.para.data.upper())).first()
                
                if not dispositivo:
                    computador = db.session.query(Computadores).join(DispositivosEquipamentos, Computadores.id==DispositivosEquipamentos.id).filter(and_(DispositivosEquipamentos.id==int(form.idDispositivo.data), DispositivosEquipamentos.idSite==int(form.idSite.data))).first()
                    print(computador)
                    flash('Mudança realizada com sucesso!', 'success')
                    return redirect(url_for('equipamento.consultaInventario', idSite=form.idSite.data))
                else:
                    dispositivo = db.session.query(DispositivosEquipamentos.id, DispositivosEquipamentos.serial, DispositivosEquipamentos.patrimonio, DispositivosEquipamentos.modelo, Sites.nome.label('site'), TipoEquipamentos.nome.label('tipo'), PontoAtendimentos.descricao).join(DispositivosEquipamentos, TipoEquipamentos.id == DispositivosEquipamentos.idTipo).join(
                        Computadores, DispositivosEquipamentos.id == Computadores.idDispositosEquipamento).join(PontoAtendimentos, Computadores.idPontoAtendimento == PontoAtendimentos.id).filter(
                        and_(DispositivosEquipamentos.idSite == int(form.idSite.data), DispositivosEquipamentos.id == int(form.idDispositivo.data))).first()
                    form.idSite.data = request.form.get('idSite')
                    form.idDispositivo.data = request.form.get('idDispositivo')
                    form.serial.data = dispositivo.serial
                    form.patrimonio.data = dispositivo.patrimonio
                    form.modelo.data = dispositivo.modelo
                    form.tipo.data = dispositivo.tipo
                    form.de.data = dispositivo.descricao
                    flash('Ponto de Atendimento já tem equipamento, remover equipamento antes de realizar mudança!', 'danger')
                    return render_template('equipamentos/mudar_Layout.html', title='Mudar Layout', legenda='Mudança de Layout', descricao='Informe para onde será movido o computador.', form=form, idSite=form.idSite.data)
                

        elif request.method == 'POST' and request.form.get('idDispositivo') and request.form.get('idSite'):
            dispositivo = db.session.query(DispositivosEquipamentos.id, DispositivosEquipamentos.serial, DispositivosEquipamentos.patrimonio, DispositivosEquipamentos.modelo, Sites.nome.label('site'), TipoEquipamentos.nome.label('tipo'), PontoAtendimentos.descricao).join(DispositivosEquipamentos, TipoEquipamentos.id==DispositivosEquipamentos.idTipo).join(
                Computadores, DispositivosEquipamentos.id==Computadores.idDispositosEquipamento).join(PontoAtendimentos, Computadores.idPontoAtendimento==PontoAtendimentos.id).filter(
                    and_(DispositivosEquipamentos.idSite == request.form.get('idSite'), DispositivosEquipamentos.id == request.form.get('idDispositivo'))).first()
            form.idSite.data = request.form.get('idSite')
            form.idDispositivo.data = request.form.get('idDispositivo')
            form.serial.data = dispositivo.serial
            form.patrimonio.data = dispositivo.patrimonio
            form.modelo.data = dispositivo.modelo
            form.tipo.data = dispositivo.tipo
            form.de.data = dispositivo.descricao
            # return redirect(url_for('equipamento.consultaInventario', idSite=request.form.get('idSite')))
            return render_template('equipamentos/mudar_Layout.html', title='Mudar Layout', legenda='Mudança de Layout', descricao='Informe para onde será movido o computador.', form=form, idSite=request.form.get('idSite'))
    else:
        abort(403)


@equipamento.route('/detalhe/<tipo_relatorio>', methods=['GET'])
@login_required
def detalhe(tipo_relatorio):
    if (current_user.permissoes[0].leitura or current_user.permissoes[0].escrita) and current_user.ativo:
        monitora = Monitora()
        if tipo_relatorio == 'Conectado':
            computadores = db.session.query(DispositivosEquipamentos.id, DispositivosEquipamentos.serial, DispositivosEquipamentos.hostname, DispositivosEquipamentos.patrimonio, Status.ativo, PontoAtendimentos.descricaoPa).join(
                DispositivosEquipamentos, Status.id == DispositivosEquipamentos.idStatus).join(PontoAtendimentos, DispositivosEquipamentos.idLocalPa == PontoAtendimentos.id).filter(Status.ativo == True).all()
        elif tipo_relatorio == 'Desconectado':
            computadores = monitora.statusDesconectado()
        else:
            computadores = monitora.statusAtencao()
        # DispositivosEquipamentoses=DispositivosEquipamentoses
        return render_template('equipamentos/detalhe.html', title='Informações - Dispositivos', legenda=f'{tipo_relatorio}')
    else:
        abort(403)

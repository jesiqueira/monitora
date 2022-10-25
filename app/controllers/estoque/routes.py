from flask import render_template, Blueprint, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user
from app.controllers.estoque.form import EstoqueViewForm, EstoqueCadastroForm, EstoqueUpdateForm, EstoqueDeleteForm, EstoqueMudarLocalForm
from app import db
from sqlalchemy import or_, and_, not_
from app.models.bdMonitora import Areas, PontoAtendimentos, Sites, Status, TipoEquipamentos, DispositivosEquipamentos, Computadores
from datetime import datetime
from pytz import timezone

est = Blueprint('est', __name__)

def preencherLayoutMudarLocal(idSite, idEquipamento, mensagem='', validation='success'):
    '''Função ira buscar se existe equipamento cadastrado e irá preencher o formulário com informações.'''
    try:
        dispositivo = db.session.query(DispositivosEquipamentos.id, DispositivosEquipamentos.serial, DispositivosEquipamentos.patrimonio, DispositivosEquipamentos.modelo, Sites.nome.label('site'), Sites.id.label('idSite'), TipoEquipamentos.nome.label('tipo')).join(
            DispositivosEquipamentos, Sites.id == DispositivosEquipamentos.idSite).join(TipoEquipamentos, DispositivosEquipamentos.idTipo == TipoEquipamentos.id).filter(and_(DispositivosEquipamentos.id == idEquipamento), DispositivosEquipamentos.idSite == idSite).first()
        areas = db.session.query(Areas).join(Areas.site).filter(
            and_(Sites.id == dispositivo.idSite, not_(Areas.nome == 'Estoque'))).all()
    except Exception as e:
        print(f'Error: {e}')
    
    form = EstoqueMudarLocalForm()
    form.idSite.data = dispositivo.idSite
    form.idEquipamento.data = dispositivo.id
    form.serial.data = dispositivo.serial
    form.patrimonio.data = dispositivo.patrimonio
    form.modelo.data = dispositivo.modelo
    form.tipo.data = dispositivo.tipo
    form.local.choices = list(map(lambda area: area.nome, areas))
    flash(mensagem, validation)
    return render_template('estoque/estoque_mudarLocal.html', title='Mudar local', legenda='Mudar Local do Equipamento', descricao=f'{dispositivo.site} - Selecione o local para onde vai mudar esse Dispositivo/Equipamento.', form=form, idSite=dispositivo.idSite)


@est.route('/mudarLocal', methods=['GET', 'POST'])
@login_required
def mudarLocal():
    if (current_user.permissoes[0].leitura or current_user.permissoes[0].escrita) and current_user.ativo:
        idDispositivo = request.form.get('idEstoque')
        siteId = request.form.get('idSite')
        form = EstoqueMudarLocalForm()

        if form.validate_on_submit():
            if form.local.data == 'Inventario':
                if not form.pa.data:
                    return preencherLayoutMudarLocal(idSite=form.idSite.data, idEquipamento=form.idEquipamento.data, mensagem='Por favor, preencher o campo Ponto de Atendimento', validation='warning')
                else:
                    try:
                        pa = db.session.query(PontoAtendimentos.descricao, PontoAtendimentos.idSite, Sites.nome).join(Sites, Sites.id==PontoAtendimentos.idSite).filter(PontoAtendimentos.descricao==form.pa.data).first()
                        if not pa:
                            return preencherLayoutMudarLocal(idSite=form.idSite.data, idEquipamento=form.idEquipamento.data, mensagem='Ponto de Atendimento não Cadastrado', validation='danger')
                        else:
                            computador = db.session.query(DispositivosEquipamentos.serial, PontoAtendimentos.descricao, Areas.nome).join(Computadores, DispositivosEquipamentos.id==Computadores.idDispositosEquipamento).join(PontoAtendimentos, Computadores.idPontoAtendimento==PontoAtendimentos.id).join(Areas, DispositivosEquipamentos.idArea==Areas.id).filter(and_(DispositivosEquipamentos.idSite==form.idSite.data, PontoAtendimentos.descricao==form.pa.data)).first()
                            if not computador:
                                if pa.idSite == form.idSite.data:
                                    area = db.session.query(Areas).join(Areas.site).filter(and_(Sites.id == form.idSite.data, Areas.nome == form.local.data)).first()
                                    equipamento = DispositivosEquipamentos.query.get(form.idEquipamento.data)
                                    equipamento.idArea = area.id

                                    data_e_hora_atuais = datetime.now()
                                    fuso_horario = timezone('America/Sao_Paulo')
                                    data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)

                                    status = Status(ativo=True, dataHora=data_e_hora_sao_paulo)
                                    db.session.add(status)
                                    db.session.commit()

                                    computador = Computadores(idDispositosEquipamento=equipamento.id, idPontoAtendimento=pa.id, idStatus=status.id)
                                    db.session.add(computador)
                                    db.session.commit()

                                    flash('Direcionado para Inventário com sucesso!', 'success')
                                    return redirect(url_for('est.estoqueConsulta', idSite=form.idSite.data))
                                else:
                                    flash('Ponto de Atendimento não pertence site.', 'danger')
                            else:
                                flash('Já existe um dispositivo/equipamento cadastrado nesse local, por favor, fazer as correções!', 'danger')
                    except Exception as e:
                        # print(f'Error: {e}')
                        db.session.flush()
                        db.session.rollback()
            elif form.local.data == 'Descarte':
                try:
                    area = db.session.query(Areas).join(Areas.site).filter(and_(Sites.id==form.idSite.data, Areas.nome==form.local.data)).first()
                    equipamento = DispositivosEquipamentos.query.get(form.idEquipamento.data)
                    equipamento.idArea = area.id
                    db.session.commit()
                except Exception as e:
                    # print(f"Error: {e}")
                    db.session.flush()
                    db.session.rollback()
                flash('Direcionado para Descarte com sucesso!', 'success')
            return redirect(url_for('est.estoqueConsulta', idSite=form.idSite.data))
        elif request.method == 'POST' and idDispositivo and siteId:
            try:
                dispositivo = db.session.query(DispositivosEquipamentos.id, DispositivosEquipamentos.serial, DispositivosEquipamentos.patrimonio, DispositivosEquipamentos.modelo, Sites.nome.label('site'), TipoEquipamentos.nome.label('tipo')).join(DispositivosEquipamentos, Sites.id==DispositivosEquipamentos.idSite).join(TipoEquipamentos, DispositivosEquipamentos.idTipo==TipoEquipamentos.id).filter(and_(DispositivosEquipamentos.id==idDispositivo), DispositivosEquipamentos.idSite==siteId).first()
                areas = db.session.query(Areas).join(Areas.site).filter(and_(Sites.id==siteId,not_(Areas.nome=='Estoque'))).all()
            except Exception as e:
                # print(f'Error: {e}')
                db.session.flush()
            
            form.idSite.data = siteId
            form.idEquipamento.data = dispositivo.id
            form.serial.data = dispositivo.serial
            form.patrimonio.data = dispositivo.patrimonio
            form.modelo.data = dispositivo.modelo
            form.tipo.data = dispositivo.tipo
            form.local.choices = list(map(lambda area: area.nome, areas))
            return render_template('estoque/estoque_mudarLocal.html', title='Mudar local', legenda='Mudar Local do Equipamento', descricao=f'{dispositivo.site} - Selecione o local para onde vai mudar esse Dispositivo/Equipamento.', form=form, idSite=siteId)
    else:
        abort(403)


@est.route('/estoque/view', methods=['GET'])
@login_required
def estoqueView():
    if (current_user.permissoes[0].leitura or current_user.permissoes[0].escrita) and current_user.ativo:
        form = EstoqueViewForm()
        try:
            sites = db.session.query(Sites).all()
        except Exception as e:
            print(f'Error: {e}')
        return render_template('estoque/estoque_view.html', title='Local Estoque', legenda='Estoques - Mapfre(BR)', descricao='Selecione o Site abaixo para acessar estoque.', sites=sites, form=form)
    else:
        abort(403)


@est.route('/estoque/<int:idSite>/consulta', methods=['GET'])
@login_required
def estoqueConsulta(idSite):
    if (current_user.permissoes[0].leitura or current_user.permissoes[0].escrita) and current_user.ativo:
        form = EstoqueViewForm()
        try:
            site = Sites.query.get(idSite)
        except Exception as e:
            # print(f'Erro: {e}')
            db.session.flush()
        db.session.flush()
        dispositivosEstoque = db.session.query(DispositivosEquipamentos.id, DispositivosEquipamentos.serial, DispositivosEquipamentos.patrimonio, TipoEquipamentos.nome).join(
            DispositivosEquipamentos, TipoEquipamentos.id == DispositivosEquipamentos.idTipo).join(Areas, DispositivosEquipamentos.idArea == Areas.id).filter(and_(DispositivosEquipamentos.idSite == idSite, Areas.nome == 'Estoque')).all()
        return render_template('estoque/estoque.html', title='Estoque', legenda=f'Estoque - {site.nome}', descricao='Relação de todos os Dispositivos/Equipamentos cadastrado no estoque.', idSite=idSite, form=form, dispositivosEstoque=dispositivosEstoque)
    else:
        abort(403)


@est.route('/estoque/<int:idSite>/cadastro', methods=['GET', 'POST'])
@login_required
def estoqueCadastro(idSite):
    if (current_user.permissoes[0].leitura or current_user.permissoes[0].escrita) and current_user.ativo:
        form = EstoqueCadastroForm()
        try:
            site = Sites.query.get(idSite)
        except Exception as e:
            print(f'Erro: {e}')
        if form.validate_on_submit():
            # equipamento = db.session.query(TipoEquipamentos).join(TipoEquipamentos.site).filter(and_(TipoEquipamentos.nome==form.nome.data, Sites.id==idSite)).first()
            if not form.serial.data and not form.patrimonio.data:
                flash(
                    'Todos os campos estão vázio, preenchar ao menos um campo, Serial ou Patrimônio!', 'danger')
                return redirect(url_for('est.estoqueCadastro', idSite=idSite))
            else:
                try:
                    # Verifica se já existe equipamento cadastrado
                    equipamento = db.session.query(DispositivosEquipamentos.serial, DispositivosEquipamentos.patrimonio, Areas.nome, Sites.nome.label('site')).join(DispositivosEquipamentos, Areas.id == DispositivosEquipamentos.idArea).join(
                        Sites, DispositivosEquipamentos.idSite == Sites.id).filter(and_(Areas.nome == 'Estoque', or_(DispositivosEquipamentos.serial == form.serial.data.upper(), DispositivosEquipamentos.patrimonio == form.patrimonio.data.upper()))).first()
                    # print(equipamento)
                    if not equipamento:
                        try:
                            area = db.session.query(Areas).filter_by(
                                nome='Estoque').first()
                        except Exception as e:
                            print(f'Error: {e}')
                        try:
                            tipo = db.session.query(TipoEquipamentos).join(TipoEquipamentos.site).filter(
                                and_(TipoEquipamentos.nome == form.tipo.data, Sites.id == idSite)).first()
                        except Exception as e:
                            print(f'Error: {e}')

                        if area and tipo:
                            estoque = DispositivosEquipamentos(serial=form.serial.data.upper(), hostname='', patrimonio=form.patrimonio.data.upper(), modelo=form.modelo.data.title(
                            ), processador=form.processador.data.title(), fabricante=form.fabricante.data.title(), idArea=area.id, idSite=site.id, idTipo=tipo.id)
                            db.session.add(estoque)
                            db.session.commit()
                            flash('Equipamento cadastrado com sucesso.', 'success')
                            return redirect(url_for('est.estoqueConsulta', idSite=idSite))
                    else:
                        flash(
                            f'Equipamento já cadastrado no Estoque em {equipamento.site}!', 'danger')
                        return redirect(url_for('est.estoqueCadastro', idSite=idSite))

                except Exception as e:
                    print(f'Error ao buscar: {e}')
                return redirect(url_for('est.estoqueConsulta', idSite=idSite))
        else:
            tipoEquipamento = db.session.query(TipoEquipamentos).join(
                TipoEquipamentos.site).filter(Sites.id == idSite).all()
            form.tipo.choices = list(
                map(lambda tipo: tipo.nome, tipoEquipamento))
            return render_template('estoque/estoque_cadastro.html', title='Cadastrar Novo Equipamento', legenda='Cadastrar Equipamento - Estoque', descricao=f'Preenchar campos para cadastrar novo equipamento no estoque de: {site.nome}', form=form, idSite=idSite)
    else:
        abort(403)


@est.route('/updateEstoque', methods=['POST'])
@login_required
def updateEstoque():
    if (current_user.permissoes[0].leitura or current_user.permissoes[0].escrita) and current_user.ativo:
        form = EstoqueUpdateForm()
        if form.validate_on_submit():
            db.session.flush()
            estoque = db.session.query(DispositivosEquipamentos).filter(and_(DispositivosEquipamentos.id == form.idEstoque.data, DispositivosEquipamentos.idSite == form.idSite.data)).first()
            
            estoque.serial = form.serial.data
            estoque.patrimonio = form.patrimonio.data
            estoque.modelo = form.modelo.data
            estoque.processador = form.processador.data
            estoque.fabricante = form.fabricante.data
            tipo = db.session.query(TipoEquipamentos).join(TipoEquipamentos.site).filter(and_(Sites.id == form.idSite.data, TipoEquipamentos.nome==form.tipo.data)).first()
            estoque.idTipo = tipo.id
            db.session.commit()
            flash('Dados atualizado com sucesso.', 'success')
            return redirect(url_for('est.estoqueConsulta', idSite=form.idSite.data))
        elif request.method == 'POST' and request.form.get('idEstoque') and request.form.get('idSite'):
            # print(f"ID Estoque:{request.form.get('idEstoque')}")
            # print(f"ID Site:{request.form.get('idSite')}")
            try:
                estoque = db.session.query(DispositivosEquipamentos).filter(and_(DispositivosEquipamentos.id == request.form.get(
                    'idEstoque'), DispositivosEquipamentos.idSite == request.form.get('idSite'))).first()
                tipo = db.session.query(TipoEquipamentos).join(
                    TipoEquipamentos.site).filter(Sites.id == request.form.get('idSite')).all()
                form.idSite.data = request.form.get('idSite')
                form.idEstoque.data = request.form.get('idEstoque')
                form.serial.data = estoque.serial
                form.patrimonio.data = estoque.patrimonio
                form.fabricante.data = estoque.fabricante
                form.modelo.data = estoque.modelo
                form.processador.data = estoque.processador
                form.tipo.choices = list(map(lambda tipo: tipo.nome, tipo))
            except Exception as e:
                print(f'Error: {e}')
            return render_template('estoque/estoque_update.html', title='Atualizar Estoque', legenda='Atualizar Estoque', descricao='Modificar os dados dos campos abaixo para atualizar', form=form, idSite=request.form.get('idSite'))


@est.route('/deleteEstoque', methods=['POST'])
@login_required
def deleteEstoque():
    if (current_user.permissoes[0].leitura or current_user.permissoes[0].escrita) and current_user.ativo:
        form = EstoqueDeleteForm()
        db.session.flush()
        if form.validate_on_submit():
            estoque = db.session.query(DispositivosEquipamentos).filter(and_(DispositivosEquipamentos.id == form.idEstoque.data, DispositivosEquipamentos.idSite == form.idSite.data)).first()
            db.session.delete(estoque)
            db.session.commit()
            flash('Equipamento/Dispositivo removido com sucesso.', 'success')
            return redirect(url_for('est.estoqueConsulta', idSite=form.idSite.data))
        elif request.method == 'POST' and request.form.get('idEstoque') and request.form.get('idSite'):
            try:
                estoque = db.session.query(DispositivosEquipamentos).filter(and_(DispositivosEquipamentos.id == request.form.get(
                    'idEstoque'), DispositivosEquipamentos.idSite == request.form.get('idSite'))).first()
                tipo = db.session.query(TipoEquipamentos).join(
                    TipoEquipamentos.site).filter(Sites.id == request.form.get('idSite')).all()
                form.idSite.data = request.form.get('idSite')
                form.idEstoque.data = request.form.get('idEstoque')
                form.serial.data = estoque.serial
                form.patrimonio.data = estoque.patrimonio
                form.fabricante.data = estoque.fabricante
                form.modelo.data = estoque.modelo
                form.processador.data = estoque.processador
                form.tipo.choices = list(map(lambda tipo: tipo.nome, tipo))
            except Exception as e:
                print(f'Error: {e}')
            return render_template('estoque/estoque_delete.html', title='Atualizar Estoque', legenda='Remover Dispositivo Estoque', descricao='Está certo que deseja remover Equipamento/Dispositivo do Estoque', form=form, idSite=request.form.get('idSite'))

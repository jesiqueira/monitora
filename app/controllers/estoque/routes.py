from turtle import title
from flask import render_template, Blueprint, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user
from app.controllers.estoque.form import EstoqueViewForm, EstoqueCadastroForm, EstoqueUpdateForm, EstoqueDeleteForm
from app import db
from sqlalchemy import or_, and_
from app.models.bdMonitora import Areas, Sites, TipoEquipamentos, DispositivosEquipamentos

est = Blueprint('est', __name__)


@est.route('/estoque')
@login_required
def estoque():
    if (current_user.permissoes[0].leitura or current_user.permissoes[0].escrita) and current_user.ativo:
        return render_template('estoque/estoque.html', title='Estoque', legenda='Equipamento no estoque')
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
        return render_template('estoque/estoque_view.html', title='Area', legenda='Estoques - Mapfre(BR)', descricao='Selecione o Site abaixo para acessar estoque.', sites=sites, form=form)
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
            print(f'Erro: {e}')
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

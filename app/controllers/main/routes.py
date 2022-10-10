from flask import render_template, flash, redirect, url_for, Blueprint, request, abort
from app.controllers.main.form import (
    SiteForm, LocalAtendimento, SiteUpdateForm, UpdateLocal, AreaForm)
from flask_login import current_user, login_required
from app.models.bdMonitora import Enderecos, Sites, PontoAtendimentos, Areas
from app import db
from sqlalchemy import exc, and_
from app.controllers.equipamento.monitora import Monitora
from datetime import date, datetime


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
@main.route('/monitora')
def home():
    # print(current_user.id)
    monitora = Monitora()
    return render_template('main/home.html', title='Home', local='São Carlos', computador=monitora.computadoresView())


@main.route('/site')
@login_required
def site():
    if current_user.permissoes[0].permissao == 'w' and current_user.ativo:
        sites = db.session.query(Sites.id, Sites.nome, Enderecos.rua, Enderecos.cep, Enderecos.cidade).join(
            Sites, Enderecos.id == Sites.id).all()
        print(sites)
        return render_template('main/site.html', title='Site', sites=sites)
    else:
        abort(403)


@main.route('/site/new', methods=['GET', 'POST'])
@login_required
def registrar_site():
    if current_user.permissoes[0].permissao == 'w' and current_user.ativo:
        form = SiteForm()
        if form.validate_on_submit():
            endereco = Enderecos(cidade=form.cidade.data, rua=form.rua.data, cep=form.cep.data)
            db.session.add(endereco)
            db.session.commit()
            site = Sites(form.nome.data, endereco.id)
            db.session.add(site)
            db.session.commit()
            flash('Site Cadastrado com sucesso!', 'success')
            return redirect(url_for('main.site'))
        return render_template('main/registrar_site.html', title='Registrar Site', form=form)
    else:
        abort(403)


@main.route('/site/<int:id_site>/update', methods=['GET', 'POST'])
@login_required
def update_site(id_site):
    if current_user.permissoes[0].permissao == 'w' and current_user.ativo:
        try:
            endereco = Enderecos.query.get_or_404(id_site)
            site = Sites.query.filter_by(idEndereco=endereco.id).first_or_404()
        except Exception as e:
            print(f'Erro ao consultar: {e}')
        form = SiteUpdateForm()
        if form.validate_on_submit():
            endereco.rua = form.rua.data
            endereco.cep = form.cep.data
            endereco.cidade = form.cidade.data
            site.nome = form.nome.data
            db.session.commit()
            flash('Dados atualizados com sucesso', 'success')
            return redirect(url_for('main.site'))
        elif request.method == 'GET':
            form.rua.data = endereco.rua
            form.cep.data = endereco.cep
            form.cidade.data = endereco.cidade
            form.nome.data = site.nome
        return render_template('main/update_site.html', title='Update Site', legenda='Editar Site', id_site=id_site, form=form)
    else:
        abort(403)


@main.route('/site/delete', methods=['POST'])
@login_required
def delete_site():
    if current_user.permissoes[0].permissao == 'w' and current_user.ativo:
        id_site = request.form.get('id_site')
        endereco = Enderecos.query.get_or_404(id_site)
        site = Sites.query.filter_by(idEndereco=endereco.id).first_or_404()
        if site.id != 1:
            db.session.delete(endereco)
            db.session.delete(site)
            db.session.commit()
            flash('Site removido conforme solicitado', 'success')
        else:
            flash('Restrição de segurança - Site não pode ser removido', 'danger')
        return redirect(url_for('main.site'))
    else:
        abort(403)


@main.route('/local', methods=['GET', 'POST'])
@login_required
def localizarPA():
    if current_user.permissoes[0].permissao == 'w' and current_user.ativo:
        locais = db.session.query(PontoAtendimentos.id, PontoAtendimentos.descricao, Sites.nome).join(
            PontoAtendimentos, Sites.id == PontoAtendimentos.idSite).all()
        return render_template('main/local.html', title='Ponto Atendimento', locais=locais)
    else:
        abort(403)


@main.route('/local/registrarLocal', methods=['GET', 'POST'])
@login_required
def registrarLocal():
    if current_user.permissoes[0].permissao == 'w' and current_user.ativo:
        form = LocalAtendimento()
        if form.validate_on_submit():
            site = Sites.query.filter_by(nome=form.localSelect.data).first()
            if site:
                local = PontoAtendimentos(
                    descricao=form.localPa.data, idSite=site.id)
                db.session.add(local)
                db.session.commit()
                flash('Ponto de atendimento cadastrado com sucesso', 'success')
                return redirect(url_for('main.localizarPA'))
            else:
                flash('Ponto de atendimento cadastrado com sucesso', 'danger')
                return redirect(url_for('main.registrarPa'))
    else:
        abort(403)

    return render_template('main/create_ponto_atendimento.html', title='Novo Ponto Atendimento', form=form)


@main.route('/local/<int:id_local>/update', methods=['GET', 'POST'])
@login_required
def updateLocal(id_local):
    if current_user.permissoes[0].permissao == 'w' and current_user.ativo:
        form = UpdateLocal()
        try:
            localForm = db.session.query(PontoAtendimentos.descricaoPa, PontoAtendimentos.idSite, PontoAtendimentos.id, Sites.nome).join(
                Sites, Sites.id == PontoAtendimentos.idSite).filter(PontoAtendimentos.id == id_local).first_or_404()
            # print(local)
            # precisa verificar a consulta para atualizar local e o site
        except Exception as e:
            print(f'Erro ao realizar consulta{e}')
            abort(404)
        if form.validate_on_submit():
            try:
                local = PontoAtendimentos.query.get_or_404(id_local)
                site = Sites.query.filter(Sites.nome == form.localSelect.data).first_or_404()
            except Exception as e:
                # print(f'Erro ao realizar consulta: {e}')
                abort(404)
            local.idSite = site.id
            local.localizadoEm = form.localPa.data
            try:
                db.session.commit()
                flash('Local atualizado com sucesso', 'success')
                return redirect(url_for('main.localizarPA'))
            except exc.IntegrityError as e:
                # print(f'Erro de integridade chave unique: {e}')
                flash('Local já cadastrado! Verificar dados inseridos.', 'danger')
                db.session.flush()
                db.session.rollback()

        elif request.method == 'GET':
            form.localPa.data = localForm.descricaoPa
            form.localSelect.data = localForm.nome

        return render_template('main/update_local.html', title='Update Ponto Atendimento', form=form)
    else:
        abort(403)

# Falta fazer opção para excluir localPa


@main.route('/home/AtualizarComputadorSite', methods=['GET'])
@login_required
def atualizarComputadorSite():
    if current_user.permissoes[0].permissao == 'w' and current_user.ativo:
        monitora = Monitora()
        monitora.threadAtualizarStatusComputador()
        flash('Dados Atualizado com sucesso!', 'success')
        return redirect(url_for('main.home'))
    else:
        abort(403)


@main.route('/area/nova', methods=['GET', 'POST'])
@login_required
def area():
    if current_user.permissoes[0].permissao == 'w' and current_user.ativo:
        form = AreaForm()
        if form.validate_on_submit():
            try:
                print(f'Area: {form.area.data}, Site: {form.localSelect.data}')
                area = db.session.query(Areas.nome, Sites.nome).join(Areas.site).filter(and_(Sites.nome == form.localSelect.data, Areas.nome == form.area.data)).first()
                if area:
                    flash(f'{form.area.data} já está cadastrada para  {form.localSelect.data}', 'danger')
                else:
                    try:
                        site = Sites.query.filter_by(nome=form.localSelect.data).first()
                        area = Areas(nome=form.area.data, site=[site])
                        db.session.add(area)
                        db.session.commit()
                        flash('Área cadastrada com sucesso!', 'success')
                    except Exception as e:
                        print(f'Error: {e}')
            except Exception as e:
                print(f'Error: {e}')
            
            return redirect(url_for('main.areaView'))

        return render_template('main/create_area.html', title='Area', descricao='Cadastrar nova área', form=form)
    else:
        abort(403)


@main.route('/area/view', methods=['GET'])
@login_required
def areaView():
    if current_user.permissoes[0].permissao == 'w' and current_user.ativo:
        areas = db.session.query(Areas.id, Areas.nome, Sites.nome.label('site')).join(Areas.site).all()
        return render_template('main/listar_area.html', title='Area', descricao='Relação das área', areas=areas)
    else:
        abort(403)

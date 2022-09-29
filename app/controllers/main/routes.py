from flask import render_template, flash, redirect, url_for, Blueprint, request, abort
from app.controllers.main.form import (SiteForm, LocalAtendimento, SiteUpdateForm, UpdateLocal)
from flask_login import current_user, login_required
from app.models.bdMonitora import Endereco, Site, LocalPa
from app import db
from sqlalchemy import exc
from app.controllers.equipamento.monitora import Monitora
from datetime import date, datetime


main = Blueprint('main', __name__)

desktop = {
    'patrimônio': '56233',
    'conectado': 1500,
    'hora': 10,
    'min': 30,
    'seg': 25,
    'data': '10/06/2022',
    'desconectado': 10,
    'atencao': 2
}


@main.route('/')
@main.route('/home')
@main.route('/monitora')
def home():
    # print(current_user.id)
    monitora = Monitora()
    # monitora.threadAtualizarStatusComputador()
    monitora.calculaHora() 
    return render_template('main/home.html', title='Home', local='São Carlos', desktop=desktop, computador=monitora.computadoresView())


@main.route('/site')
@login_required
def site():
    if current_user.admin and current_user.ativo:
        sites = db.session.query(Site.id, Site.nome, Endereco.rua, Endereco.cep, Endereco.cidade).join(Site, Endereco.id == Site.id).all()
        # print(sites[0].nome)
        return render_template('main/site.html', title='Site', sites=sites)
    else:
        abort(403)


@main.route('/site/new', methods=['GET', 'POST'])
@login_required
def registrar_site():
    if current_user.admin and current_user.ativo:
        form = SiteForm()
        if form.validate_on_submit():
            endereco = Endereco(cidade=form.cidade.data, rua=form.rua.data, cep=form.cep.data)
            db.session.add(endereco)
            db.session.commit()
            site = Site(form.nome.data, endereco.id)
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
    if current_user.admin and current_user.ativo:
        try:
            endereco = Endereco.query.get_or_404(id_site)
            site =Site.query.filter_by(idEndereco=endereco.id).first_or_404()
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
        return render_template('main/update_site.html', title='Update Site', legenda ='Editar Site', id_site=id_site, form=form)
    else:
        abort(403)

@main.route('/site/delete', methods=['POST'])
@login_required
def delete_site():
    if current_user.admin and current_user.ativo:
        id_site = request.form.get('id_site')
        endereco = Endereco.query.get_or_404(id_site)
        site =Site.query.filter_by(idEndereco=endereco.id).first_or_404()
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
    if current_user.admin and current_user.ativo:
        locais = db.session.query(LocalPa.id, LocalPa.descricaoPa, Site.nome).join(LocalPa, Site.id == LocalPa.idSite).all()
        return render_template('main/local.html', title='Ponto Atendimento', locais=locais)
    else:
        abort(403)


@main.route('/local/registrarLocal', methods=['GET', 'POST'])
@login_required
def registrarLocal():
    if current_user.admin and current_user.ativo:
        form = LocalAtendimento()
        if form.validate_on_submit():
            site = Site.query.filter_by(nome=form.localSelect.data).first()
            if site:
                local = LocalPa(form.localPa.data, site.id)
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
    if current_user.admin and current_user.ativo:
        form = UpdateLocal()
        try:
            localForm = db.session.query(LocalPa.descricaoPa, LocalPa.idSite, LocalPa.id, Site.nome).join(Site, Site.id == LocalPa.idSite).filter(LocalPa.id==id_local).first_or_404()
            # print(local)
            # precisa verificar a consulta para atualizar local e o site
        except Exception as e:
            print(f'Erro ao realizar consulta{e}')
            abort(404)
        if form.validate_on_submit():
            try:
                local = LocalPa.query.get_or_404(id_local)
                site = Site.query.filter(Site.nome == form.localSelect.data).first_or_404()
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
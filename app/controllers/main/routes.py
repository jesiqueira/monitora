from flask import render_template, flash, redirect, url_for, Blueprint
from app.controllers.main.form import SiteForm, LocalAtendimento
from flask_login import current_user, login_required
from app.models.bdMonitora import Endereco, Site, Local
from app import db


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
    return render_template('home.html', title='Home', local='São Carlos', desktop=desktop)


@main.route('/site')
@login_required
def site():
    sites = db.session.query(Site.id, Site.siteNome, Endereco.rua, Endereco.cep, Endereco.cidade).join(Site, Endereco.id == Site.id).all()
    return render_template('site.html', title='Site', sites=sites)


@main.route('/site/new', methods=['GET', 'POST'])
@login_required
def registrar_site():
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
    return render_template('registrar_site.html', title='Registrar Site', form=form)

@main.route('/site/local', methods=['GET', 'POST'])
@login_required
def localizarPA():
    locais = db.session.query(Local.id, Local.localizadoEm, Site.siteNome).join(Local, Site.id == Local.idSite).all()
    return render_template('local.html', title='Ponto Atendimento', locais=locais)


@main.route('/site/registrarLocal', methods=['GET', 'POST'])
@login_required
def registrarLocal():
    form = LocalAtendimento()
    if form.validate_on_submit():
        site = Site.query.filter_by(siteNome=form.localSelect.data).first()
        if site:
            local = Local(form.localPa.data, site.id)
            db.session.add(local)
            db.session.commit()
            flash('Ponto de atendimento cadastrado com sucesso', 'success')
            return redirect(url_for('main.localizarPA'))
        else:
            flash('Ponto de atendimento cadastrado com sucesso', 'danger')
            return redirect(url_for('main.registrarPa'))

    return render_template('create_ponto_atendimento.html', title='Novo Ponto Atendimento', form=form)
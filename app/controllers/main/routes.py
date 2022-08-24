from flask import render_template, flash, redirect, url_for, Blueprint
from app.controllers.main.form import SiteForm
from flask_login import current_user, login_required
from app.models.bdMonitora import Endereco, Site
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

@main.route('/site/pa', methods=['GET', 'POST'])
@login_required
def localizarPA():
    return render_template('localizacaoPa.html', title='Ponto Atendimento')
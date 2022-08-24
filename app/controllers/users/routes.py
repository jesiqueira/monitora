from flask import render_template, flash, redirect, url_for, Blueprint, request
from app.controllers.users.form import LoginForm, CreateUserForm
from app import db, bcrypt
from app.models.bdMonitora import Usuario, Endereco, Site
from flask_login import login_user, current_user, logout_user, login_required


user = Blueprint('user', __name__)


@user.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = Usuario.query.filter_by(login=form.login.data).first()
        if user and bcrypt.check_password_hash(user.senha, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Error, Verifique Login/Senha!', 'danger')

    return render_template('login.html', title='Login', form=form)


@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@user.route('/createAdmin')
def createAdmin():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    hashed_password = bcrypt.generate_password_hash(
        '#mapfre@1234#').decode('utf-8')

    admin = Usuario.query.all()

    if len(admin) == 0:
        endereco = Endereco()
        db.session.add(endereco)

        site = Site(idEndereco=1)
        db.session.add(site)

        user = Usuario('Administrador', 'Admin', hashed_password,
                       'Administrador@email.com.br', 1)
        db.session.add(user)
        db.session.commit()
        flash('Login Administrador criado com sucesso!', 'success')
        return redirect(url_for('main.home'))
    else:
        flash('Login Administrador já existe!', 'danger')
        return redirect(url_for('main.home'))

@user.route('/usuarios')
@login_required
def lista_usuario():
    users = db.session.query(Usuario.id, Usuario.userNome, Usuario.login, Usuario.email, Site.siteNome).join(Usuario, Site.id == Usuario.idSite).all()
    # print(users[1].siteNome)
    return render_template('usuario.html', title='Usuários', usuarios=users)

@user.route('/usuario/novo',  methods=['GET', 'POST'])
@login_required
def novo_usuario():
    form = CreateUserForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        site = Site.query.filter_by(siteNome=form.siteSelect.data).first_or_404(description=f'Site {site.siteNome} não localizado, verifique se está cadastrado!')
        user = Usuario(nome=form.nome.data, login=form.login.data, senha=hashed_password, email=form.email.data, idSite=site.id)
        db.session.add(user)
        db.session.commit()
        flash(f'Conta criada com sucesso para: {form.nome.data}!', 'success')
        return redirect(url_for('user.lista_usuario'))
    
    return render_template('criar_usuario.html', title='Novo usuário', form=form)
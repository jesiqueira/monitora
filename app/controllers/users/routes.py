from flask import render_template, flash, redirect, url_for, Blueprint, request, abort
from app.controllers.users.form import (LoginForm, CreateUserForm, UpdateUserForm, UpdatePassWordUserForm)
from app import db, bcrypt
from app.models.bdMonitora import (Usuario, Endereco, Site)
from flask_login import login_user, current_user, logout_user, login_required


user = Blueprint('user', __name__)


@user.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    try:
        user = Usuario.query.filter_by(login=form.login.data).first()
        if form.validate_on_submit():
            if user and bcrypt.check_password_hash(user.senha, form.password.data) and user.ativo:
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
            elif not user.ativo:
                abort(403)
            else:
                flash('Error, Verifique Login/Senha!', 'danger')

    except Exception as e:
        # print(f'Erro que vou ver qual é: {e}')
        abort(403)
    
    return render_template('users/login.html', title='Login', form=form)


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
                       'Administrador@email.com.br', True, True, 1)
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
    if current_user.admin and current_user.ativo:
        users = db.session.query(Usuario.id, Usuario.userNome, Usuario.login, Usuario.email, Site.siteNome).join(Usuario, Site.id == Usuario.idSite).all()
        # print(users[1].siteNome)
        return render_template('users/usuario.html', title='Usuários', usuarios=users)
    else:
        abort(403)

@user.route('/usuario/novo',  methods=['GET', 'POST'])
@login_required
def novo_usuario():
    if current_user.admin and current_user.ativo:
        form = CreateUserForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            site = Site.query.filter_by(siteNome=form.siteSelect.data).first_or_404()
            if site:
                user = Usuario(nome=form.nome.data, login=form.login.data, senha=hashed_password, email=form.email.data, admin=form.admin.data, ativo=form.ativo.data ,idSite=site.id)
                db.session.add(user)
                db.session.commit()
                flash(f'Conta criada com sucesso para: {form.nome.data}!', 'success')
            return redirect(url_for('user.lista_usuario'))
        
        return render_template('users/criar_usuario.html', title='Novo usuário', form=form)
    else:
        abort(403)

@user.route('/usuario/<int:id_user>/update',  methods=['GET', 'POST'])
@login_required
def update_usuario(id_user):
    if current_user.admin and current_user.ativo:
        try:
            user = Usuario.query.get_or_404(id_user)
        except Exception as e:
            # print(f'Erro ao consultar usuário {e}')
            abort(404)        
        form = UpdateUserForm()
        if form.validate_on_submit():
            user.userNome = form.nome.data
            user.login = form.login.data
            user.email = form.email.data
            user.admin = form.admin.data
            user.ativo = form.ativo.data
            db.session.commit()
            flash('Dados atualizados com sucesso', 'success')
            return redirect(url_for('user.lista_usuario'))
        elif request.method == 'GET':
            form.nome.data = user.userNome
            form.login.data = user.login
            form.email.data = user.email
            form.admin.data = user.admin
            form.ativo.data = user.ativo
        return render_template('users/update_usuario.html', title='Editar usuário', legenda='Update dados do Usuário', form=form)
    else:
        abort(403)

@user.route('/atualizarSenha',  methods=['POST'])
@login_required
def updatePassword():
    if current_user.admin and current_user.ativo:
        form = UpdatePassWordUserForm()
        if request.method == 'POST':
            form.id_user.data = request.form.get('id_users')
            return render_template('users/passWord_usuario.html', title='Editar Senha', legenda='Atualizar senha do Usuário', form=form)
    else:
        abort(403)

@user.route('/atualizaSenhaUsuario',  methods=['POST'])
@login_required
def updatePassword_usuario():
    if current_user.admin and current_user.ativo:
        form = UpdatePassWordUserForm()
        try:
            user = Usuario.query.get_or_404(form.id_user.data)
        except Exception as e:
            abort(404)        
        if form.validate_on_submit():
            user.senha = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            db.session.commit()
            flash('Senha atualizados com sucesso', 'success')
            return redirect(url_for('user.lista_usuario'))
        return render_template('users/passWord_usuario.html', title='Editar Senha', legenda='Atualizar senha do Usuário', form=form)
    else:
        abort(403)
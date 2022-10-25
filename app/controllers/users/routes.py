from operator import and_, or_
from flask import render_template, flash, redirect, url_for, Blueprint, request, abort
from app.controllers.users.form import (LoginForm, CreateUserForm, UpdateUserForm, UpdatePassWordUserForm)
from app.controllers.main.form import Areas
from app import db, bcrypt
from sqlalchemy import or_, and_
from app.models.bdMonitora import (Permissoes, Users, Enderecos, Sites)
from flask_login import login_user, current_user, logout_user, login_required


user = Blueprint('user', __name__)


@user.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    try:
        if form.validate_on_submit():
            user = Users.query.filter_by(login=form.login.data.lower()).first_or_404()
            if user and bcrypt.check_password_hash(user.senha, form.password.data.lower()) and user.ativo:
                login_user(user=user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
            elif not user.ativo:
                abort(403)
            else:
                flash('Error, Verifique Login/Senha!', 'danger')
    except Exception as e:
        print(f'Erro que vou ver qual é: {e}')
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

    hashed_password = bcrypt.generate_password_hash('#mapfre@1234#').decode('utf-8')

    users = Users.query.all()

    if not users:
        try:
            endereco = Enderecos(rua='Coronel Jose Augusto de Oliveira Salles', cidade='São Carlos - SP', cep=13570820)
            db.session.add(endereco)
            db.session.commit()
        except Exception as e:
            db.session.flush()
            db.session.rollback()
            # print(f'Erro: {e}')

        try:
            site = Sites(nome='Mapfre - (São Carlos)', idEndereco=endereco.id)
            db.session.add(site)
            db.session.commit()
            areas = ['Estoque', 'Inventario', 'Descarte']
            for area in areas:
                a = Areas(nome=area, site=[site])
                db.session.add(a)
                db.session.commit()                
        except Exception as e:
            db.session.flush()
            db.session.rollback()
            # print(f'Erro: {e}')

        try:
            permissoes = Permissoes(leitura=True, escrita=True, adminUser=True)
            db.session.add(permissoes)
            db.session.commit()
        except Exception as e:
            db.session.flush()
            db.session.rollback()
            print(f"Erro: {e}")
        
        try:
            permissoes = Permissoes.query.all()
        except Exception as e:
            db.session.flush()
            db.session.rollback()
            # print(f'Erro: {e}')

        try:
            # print(type(permissoes))
            user = Users(nome='Administrador', login='admin', senha=hashed_password, email='admin@bbmapfre.com.br', permissoes=permissoes, ativo=True, idSite=site.id)
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.flush()
            db.session.rollback()
            print(f'Erro: {e}')
        
        flash('Login Administrador criado com sucesso!', 'success')
        return redirect(url_for('main.home'))
    else:
        flash('Login Administrador já existe!', 'danger')
        return redirect(url_for('main.home'))


@user.route('/usuarios')
@login_required
def lista_usuario():

    if current_user.permissoes[0].adminUser and current_user.ativo:
        users = db.session.query(Users.id, Users.nome.label('userNome'), Users.login, Users.email, Sites.nome.label(
            'siteNome')).join(Users, Sites.id == Users.idSite).all()
        # print(users[1]['siteNome'])
        return render_template('users/usuario.html', title='Usuários', usuarios=users)
    else:
        abort(403)


@user.route('/usuario/novo',  methods=['GET', 'POST'])
@login_required
def novo_usuario():
    form = CreateUserForm()
    # permissoes = db.session.query(Permissoes).join(Users.permissoes).filter(or_(Permissoes.leitura==form.r.data, Permissoes.escrita==form.w.data, Permissoes.adminUser==form.adminUser.data)).first()
    # print(permissoes)
    if current_user.permissoes[0].adminUser and current_user.ativo:
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            try:
                permissoes = Permissoes(leitura=form.leitura.data, escrita=form.escrita.data, adminUser=form.adminUser.data)
                db.session.add(permissoes)
                db.session.commit()
            except Exception as e:
                print(f'Error: {e}')
            site = Sites.query.filter_by(nome=form.siteSelect.data).first_or_404()
            if site:
                user = Users(nome=form.nome.data.upper(), login=form.login.data.lower(), senha=hashed_password, email=form.email.data.lower(), ativo=form.ativo.data, permissoes=[permissoes], idSite=site.id)
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
    if current_user.permissoes[0].adminUser and current_user.ativo:
        try:
            # user = Users.query.get_or_404(id_user)
            user = db.session.query(Users.nome, Users.login, Users.email, Users.ativo, Permissoes.adminUser, Permissoes.escrita, Permissoes.leitura).join(Users.permissoes).filter(Users.id==id_user).first()
        except Exception as e:
            # print(f'Erro ao consultar usuário {e}')
            abort(404)
        form = UpdateUserForm()
        if form.validate_on_submit():
            user = Users.query.get(id_user)
            permissoes = db.session.query(Permissoes).join(Users.permissoes).filter(Users.id==id_user).first()
            user.nome = form.nome.data
            user.login = form.login.data
            user.email = form.email.data
            user.ativo = form.ativo.data
            permissoes.leitura = form.leitura.data
            permissoes.escrita = form.escrita.data
            permissoes.adminUser = form.adminUser.data
            user.permissoes = [permissoes]
            db.session.commit()
            flash('Dados atualizados com sucesso', 'success')
            return redirect(url_for('user.lista_usuario'))
        elif request.method == 'GET':
            form.nome.data = user.nome
            form.login.data = user.login
            form.email.data = user.email
            form.ativo.data = user.ativo
            form.adminUser.data = user.adminUser
            form.leitura.data = user.leitura
            form.escrita.data = user.escrita
        return render_template('users/update_usuario.html', title='Editar usuário', legenda='Update dados do Usuário', form=form)
    else:
        abort(403)


@user.route('/atualizarSenha',  methods=['POST'])
@login_required
def updatePassword():
    if current_user.permissoes[0].adminUser and current_user.ativo:
        form = UpdatePassWordUserForm()
        if request.method == 'POST':
            form.id_user.data = request.form.get('id_users')
            return render_template('users/passWord_usuario.html', title='Editar Senha', legenda='Atualizar senha do Usuário', form=form)
    else:
        abort(403)


@user.route('/atualizaSenhaUsuario',  methods=['POST'])
@login_required
def updatePassword_usuario():
    if current_user.permissoes[0].adminUser and current_user.ativo:
        form = UpdatePassWordUserForm()
        try:
            user = Users.query.get_or_404(form.id_user.data)
        except Exception as e:
            abort(404)
        if form.validate_on_submit():
            user.senha = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            db.session.commit()
            flash('Senha atualizados com sucesso', 'success')
            return redirect(url_for('user.lista_usuario'))
        return render_template('users/passWord_usuario.html', title='Editar Senha', legenda='Atualizar senha do Usuário', form=form)
    else:
        abort(403)

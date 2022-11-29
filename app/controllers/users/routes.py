from operator import and_, or_
from flask import render_template, flash, redirect, url_for, Blueprint, request, abort
from app.controllers.users.form import (
    LoginForm, CreateUserForm, UpdateUserForm, UpdatePassWordUserForm, SelecaoFormUser)
from app.controllers.main.form import Areas
from app import db, bcrypt
from sqlalchemy import or_, and_
from app.models.bdMonitora import (Permissoes, Users, Enderecos, Sites)
from flask_login import login_user, current_user, logout_user, login_required


user = Blueprint('user', __name__)

@user.route('/consulta', methods=['POST'])
def consulta():
    if current_user.permissoes[0].adminUser and current_user.ativo:
        form = SelecaoFormUser()
        if form.validate_on_submit():
            consulta = '%'+form.consulta.data+'%'
            selection = form.selection.data
            if selection == 'Nome':
                users = db.session.query(Users.id, Users.nome.label('userNome'), Users.login, Users.email, Sites.nome.label('siteNome')).join(Users, Sites.id == Users.idSite).filter(and_(Sites.id==form.idSite.data, Users.nome.like(consulta))).all()
            elif selection == 'Login':
                users = db.session.query(Users.id, Users.nome.label('userNome'), Users.login, Users.email, Sites.nome.label('siteNome')).join(Users, Sites.id == Users.idSite).filter(and_(Sites.id==form.idSite.data, Users.login.like(consulta))).all()
            elif selection == 'Email':
                users = db.session.query(Users.id, Users.nome.label('userNome'), Users.login, Users.email, Sites.nome.label('siteNome')).join(Users, Sites.id == Users.idSite).filter(and_(Sites.id==form.idSite.data, Users.email.like(consulta))).all()
            else:
                users = db.session.query(Users.id, Users.nome.label('userNome'), Users.login, Users.email, Sites.nome.label('siteNome')).join(Users, Sites.id == Users.idSite).filter(Sites.id == form.idSite.data).all()
            
            return render_template('users/usuario.html', title='Usuários', usuarios=users, idSite=form.idSite.data, form=form)
        else:
            users = db.session.query(Users.id, Users.nome.label('userNome'), Users.login, Users.email, Sites.nome.label('siteNome')).join(Users, Sites.id == Users.idSite).filter(Sites.id == form.idSite.data).all()
            return render_template('users/usuario.html', title='Usuários', usuarios=users, idSite=form.idSite.data, form=form)
    else:
        abort(403)
    


@user.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    try:
        if form.validate_on_submit():
            user = Users.query.filter_by(
                login=form.login.data.lower()).first_or_404()
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

    hashed_password = bcrypt.generate_password_hash(
        '#mapfre@1234#').decode('utf-8')

    users = Users.query.all()

    if not users:
        try:
            endereco = Enderecos(
                rua='Coronel Jose Augusto de Oliveira Salles', cidade='São Carlos - SP', cep=13570820)
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
            user = Users(nome='Administrador', login='admin', senha=hashed_password,
                         email='admin@bbmapfre.com.br', permissoes=permissoes, ativo=True, idSite=site.id)
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


@user.route('/usuario/site')
@login_required
def usuarioSite():
    if current_user.permissoes[0].adminUser and current_user.ativo:
        sites = Sites.query.all()
        return render_template('users/users_site.html', sites=sites, title='Site do Usuário', legenda='Lista de Sites', descricao='Selecione o Site que deseja acessar.')
    else:
        abort(403)


@user.route('/usuarios/site/<int:idSite>')
@login_required
def lista_usuario(idSite):

    if current_user.permissoes[0].adminUser and current_user.ativo:
        form = SelecaoFormUser()
        users = db.session.query(Users.id, Users.nome.label('userNome'), Users.login, Users.email, Sites.nome.label(
            'siteNome')).join(Users, Sites.id == Users.idSite).filter(Sites.id == idSite).all()
        # print(users[1]['siteNome'])
        form.idSite.data = idSite
        return render_template('users/usuario.html', title='Usuários', usuarios=users, idSite=idSite, form=form)
    else:
        abort(403)


@user.route('/usuario/novo/<int:idSite>',  methods=['GET', 'POST'])
@login_required
def novo_usuario(idSite):
    form = CreateUserForm()
    # permissoes = db.session.query(Permissoes).join(Users.permissoes).filter(or_(Permissoes.leitura==form.r.data, Permissoes.escrita==form.w.data, Permissoes.adminUser==form.adminUser.data)).first()
    # print(permissoes)
    if current_user.permissoes[0].adminUser and current_user.ativo:
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            try:
                permissoes = Permissoes(
                    leitura=form.leitura.data, escrita=form.escrita.data, adminUser=form.adminUser.data)
                db.session.add(permissoes)
                db.session.commit()
            except Exception as e:
                print(f'Error: {e}')
            site = Sites.query.filter_by(
                nome=form.siteSelect.data).first_or_404()
            if site:
                user = Users(nome=form.nome.data.upper(), login=form.login.data.lower(), senha=hashed_password,
                             email=form.email.data.lower(), ativo=form.ativo.data, permissoes=[permissoes], idSite=site.id)
                db.session.add(user)
                db.session.commit()
                flash(
                    f'Conta criada com sucesso para: {form.nome.data}!', 'success')
            return redirect(url_for('user.lista_usuario', idSite=site.id))
        else:
            site = Sites.query.get(idSite)
            form.siteSelect.choices = [site.nome]
            return render_template('users/criar_usuario.html', title='Novo usuário', form=form, idSite=idSite)
    else:
        abort(403)


@user.route('/usuarioUpdate',  methods=['GET', 'POST'])
@login_required
def update_usuario():
    if current_user.permissoes[0].adminUser and current_user.ativo:
        form = UpdateUserForm()
        if request.method == 'POST' and request.form.get('idUser') and request.form.get('idSite'):
            user = db.session.query(Users.nome, Users.login, Users.email, Users.ativo, Permissoes.adminUser, Permissoes.escrita,
                                    Permissoes.leitura).join(Users.permissoes).filter(Users.id == request.form.get('idUser')).first()
            form.idUsuario.data = request.form.get('idUser')
            form.idSite.data = request.form.get('idSite')
            form.nome.data = user.nome
            form.login.data = user.login
            form.email.data = user.email
            form.ativo.data = user.ativo
            form.adminUser.data = user.adminUser
            form.leitura.data = user.leitura
            form.escrita.data = user.escrita
            return render_template('users/update_usuario.html', title='Editar usuário', legenda='Update dados do Usuário', form=form)

        elif form.validate_on_submit():
            user = Users.query.get(form.idUsuario.data)
            permissoes = db.session.query(Permissoes).join(
                Users.permissoes).filter(Users.id == form.idUsuario.data).first()
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
            return redirect(url_for('user.lista_usuario', idSite=form.idSite.data))
    else:
        abort(403)


@user.route('/atualizarSenha',  methods=['POST'])
@login_required
def updatePassword():
    if current_user.permissoes[0].adminUser and current_user.ativo:
        form = UpdatePassWordUserForm()
        if request.method == 'POST' and request.form.get('id_users') and request.form.get('idSite'):
            form.id_user.data = request.form.get('id_users')
            form.idSite.data = request.form.get('idSite')
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
            return redirect(url_for('user.lista_usuario', idSite=form.idSite.data))
        return render_template('users/passWord_usuario.html', title='Editar Senha', legenda='Atualizar senha do Usuário', form=form)
    else:
        abort(403)

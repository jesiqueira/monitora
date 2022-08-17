from flask import render_template, flash, redirect, url_for, Blueprint
from app.controllers.users.form import LoginForm
from app import db, bcrypt
from app.models.bdMonitora import Usuarios, Endereco, Site


user = Blueprint('user', __name__)


@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        if form.login.data == 'jesiqueira' and form.password.data == 'password':
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Error, Verifique Login/Senha!', 'danger')

    return render_template('login.html', title='Login', form=form)


@user.route('/createAdmin')
def createAdmin():
    hashed_password = bcrypt.generate_password_hash('#mapfre@1234#').decode('utf-8')
    endereco = Endereco()
    db.session.add(endereco)
    db.session.commit(endereco)

    site = Site(idEndereco=0)
    db.session.add(site)
    db.session.commit(site)

    user = Usuarios('Administrador', 'Admin', hashed_password, 'Administrador@email.com.br',0)
    db.session.add(user)
    db.session.commit()
    flash('Login Adiminstrador criado com sucesso!', 'success')
    return f"hashed: {hashed_password}"

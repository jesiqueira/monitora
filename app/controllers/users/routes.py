from flask import render_template, flash, redirect, url_for, Blueprint
from app.controllers.users.form import LoginForm


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

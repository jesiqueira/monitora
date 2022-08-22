from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import current_user, login_required


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

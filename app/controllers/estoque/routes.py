from flask import render_template, Blueprint, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user

est = Blueprint('est', __name__)

@est.route('/estoque')
@login_required
def estoque():
  if current_user.permissoes[0].permissao == 'w' and current_user.ativo:
    return render_template('estoque/estoque.html', title='Estoque', legenda='Equipamento no estoque')
  else:
    abort(403)
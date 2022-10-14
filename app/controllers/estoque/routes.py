from flask import render_template, Blueprint, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user
from app.controllers.estoque.form import EstoqueViewForm
from app import db
from app.models.bdMonitora import Areas, Sites

est = Blueprint('est', __name__)

@est.route('/estoque')
@login_required
def estoque():
  if current_user.permissoes[0].permissao == 'w' and current_user.ativo:
    return render_template('estoque/estoque.html', title='Estoque', legenda='Equipamento no estoque')
  else:
    abort(403)

@est.route('/estoque/view', methods=['GET'])
@login_required
def estoqueView():
    if current_user.permissoes[0].permissao == 'w' and current_user.ativo:
        form = EstoqueViewForm()
        try:
            sites = db.session.query(Sites).all()
        except Exception as e:
            print(f'Error: {e}')
        return render_template('estoque/estoque_view.html', title='Area', legenda='Estoques', descricao='Selecione o Site abaixo para acessar estoque.', sites=sites, form=form)
    else:
        abort(403)

@est.route('/estoque/<int:idSite>/consulta', methods=['GET'])
@login_required
def estoqueConsulta(idSite):
    if current_user.permissoes[0].permissao == 'w' and current_user.ativo:
      form = EstoqueViewForm()
      # areas = db.session.query(Areas.id, Areas.nome, Sites.nome.label('site')).join(Areas.site).filter(Sites.id==idSite).all()
      areas = []
      if areas:
          return render_template('estoque/estoque.html', title='Area', legenda='Relação das áreas', descricao=f'Relação de todos as áreas cadastrado no sistema para {areas[0].site}', areas=areas, idSite=idSite, form=form)
      else:
          return render_template('estoque/estoque.html', title='Area', legenda='Relação das áreas', descricao='Não existe áreas cadastradas', areas=areas, idSite=idSite, form=form)
    else:
        abort(403)
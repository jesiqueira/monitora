from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(401)
def error_401(error):
    return render_template('errors/403.html', title='Erro 401', local='São Carlos'), 401


@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html', title='Erro 403', local='São Carlos'), 403


@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html', title='Erro 404', local='São Carlos'), 404


@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html', title='Erro 500', local='São Carlos'), 500

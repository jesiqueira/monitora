from datetime import datetime
from enum import unique
from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


class Endereco(db.Model):
    __tablename__ = 'Endereco'
    id = db.Column(db.Integer, primary_key=True)
    rua = db.Column(db.String(40), nullable=False)
    cep = db.Column(db.String(8), nullable=False)
    cidade = db.Column(db.String(40), nullable=False)
    sites = db.relationship('Site', backref='endereco', lazy=True)

    def __init__(self, cidade='Default', rua='Anônima', cep='00.000-000'):
        self.cidade = cidade
        self.rua = rua
        self.cep = cep

    def __repr__(self) -> str:
        return f"Endereco('{self.cidade}', '{self.rua}', '{self.cep}')"


class Site(db.Model):
    __tablename__ = 'Site'
    id = db.Column(db.Integer, primary_key=True)
    siteNome = db.Column(db.String(30), nullable=False, unique=True)
    usuario = db.relationship('Usuario', backref='usuario', lazy=True)
    local = db.relationship('Local', backref='local', lazy=True)
    idEndereco = db.Column(db.Integer, db.ForeignKey(
        'Endereco.id'), nullable=False)

    def __init__(self, nome='Default', idEndereco=0):
        self.siteNome = nome
        self.idEndereco = idEndereco

    def __repr__(self) -> str:
        return f"Site('{self.siteNome}')"


class Usuario(db.Model, UserMixin):
    __tablename__ = 'Usuario'
    id = db.Column(db.Integer, primary_key=True)
    userNome = db.Column(db.String(40), unique=True, nullable=False)
    login = db.Column(db.String(20), unique=True, nullable=False)
    senha = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(40), nullable=False)
    relatorios = db.relationship('Relatorio', backref='usuario', lazy=True)
    idSite = db.Column(db.Integer, db.ForeignKey('Site.id'), nullable=False)

    def __init__(self, nome='Anonima', login='default', senha='default', email='defaul@default.com.br', idSite=0):
        self.userNome = nome
        self.login = login
        self.senha = senha
        self.email = email
        self.idSite = idSite

    def __repr__(self):
        return f"Usuario('{self.userNome}', '{self.login}', '{self.email}')"


class Tipo(db.Model):
    __tablename__ = 'Tipo'
    id = db.Column(db.Integer, primary_key=True)
    tipoNome = db.Column(db.String(40), unique=True, nullable=False)
    dispositos = db.relationship('Dispositivo', backref='tipo')

    def __init__(self, nome='Anonimo'):
        self.tipoNome = nome

    def __repr__(self):
        return f"Tipo('{self.tipoNome}')"


class Local(db.Model):
    __tablename__ = 'Local'
    id = db.Column(db.Integer, primary_key=True)
    localNome = db.Column(db.String(40), unique=True, nullable=False)
    localizadoEm = db.Column(db.String(40), unique=True, nullable=False)
    dispositivo = db.relationship('Dispositivo', backref='local', lazy=True)
    idSite = db.Column(db.Integer, db.ForeignKey('Site.id'), nullable=False)

    def __init__(self, nome='Anonimo', localizadoEm='default', idSite=0):
        self.localNome = nome
        self.localizadoEm = localizadoEm
        self.idSite = idSite

    def __repr__(self) -> str:
        return f"Local('{self.localNome}, {self.localizadoEm}, {self.dispositivo}')"


class Dispositivo(db.Model):
    __tablename__ = 'Dispositivo'
    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String(40), unique=True)
    patrimonio = db.Column(db.String(40), unique=True)
    idLocal = db.Column(db.Integer, db.ForeignKey('Local.id'), nullable=False)
    idTipo = db.Column(db.Integer, db.ForeignKey('Tipo.id'), nullable=False)

    def __init__(self, serial='S4TW02Q3', patrimonio='default', idLocal=0, idTipo=0):
        self.serial = serial
        self.patrimonio = patrimonio
        self.idLocal = idLocal
        self.idTipo = idTipo

    def __repr__(self) -> str:
        return f"Dispositivo('{self.serial}', '{self.patrimonio}')"


class Acao(db.Model):
    __tablename__ = 'Acao'
    id = db.Column(db.Integer, primary_key=True)
    acaoNome = db.Column(db.String(40), unique=True, nullable=False)
    relatorio = db.relationship(
        'Relatorio', backref='acaoRelatorio', lazy=True)

    def __init__(self, nome='Default') -> None:
        self.acaoNome = nome

    def __repr__(self) -> str:
        return f"Acao('{self.acaoNome}')"


class Relatorio(db.Model):
    __tablename__ = 'Relatorio'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    serial = db.Column(db.String(40), unique=True)
    patrimonio = db.Column(db.String(40), unique=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey(
        'Usuario.id'), nullable=False)
    idAcao = db.Column(db.Integer, db.ForeignKey('Acao.id'), nullable=False)

    def __init__(self, data=datetime.utcnow, serial='S4TW02Q3', patrimonio='default', idUsuario=0, idAcao=0):
        self.data = data
        self.serial = serial
        self.patrimonio = patrimonio
        self.idUsuario = idUsuario
        self.idAcao = idAcao

    def __repr__(self) -> str:
        return f"Relatorio('{self.data}', '{self.serial}', '{self.patrimonio}')"

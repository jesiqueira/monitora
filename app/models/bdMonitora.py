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
    nome = db.Column(db.String(30), nullable=False, unique=True)
    usuario = db.relationship('Usuario', backref='usuario', lazy=True)
    local = db.relationship('Local', backref='local', lazy=True)
    idEndereco = db.Column(db.Integer, db.ForeignKey(
        'Endereco.id'), nullable=False)

    def __init__(self, nome='Default', idEndereco=0):
        self.nome = nome
        self.idEndereco = idEndereco

    def __repr__(self) -> str:
        return f"Site('{self.nome}')"


class Usuario(db.Model, UserMixin):
    __tablename__ = 'Usuario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), unique=True, nullable=False)
    login = db.Column(db.String(20), unique=True, nullable=False)
    senha = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(40), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    ativo = db.Column(db.Boolean, nullable=False, default=False)
    relatorios = db.relationship('Relatorio', backref='usuario', lazy=True)
    idSite = db.Column(db.Integer, db.ForeignKey('Site.id'), nullable=False)

    def __init__(self, nome='Anonima', login='default', senha='default', email='defaul@default.com.br', admin=False, ativo=False, idSite=0):
        self.nome = nome
        self.login = login
        self.senha = senha
        self.email = email
        self.admin = admin
        self.ativo = ativo
        self.idSite = idSite

    def __repr__(self):
        return f"Usuario('{self.userNome}', '{self.login}', '{self.email}', '{self.admin}', '{self.ativo}')"


class Local(db.Model):
    __tablename__ = 'Local'
    id = db.Column(db.Integer, primary_key=True)
    localizadoEm = db.Column(db.String(40), unique=True, nullable=False)
    Equipamento = db.relationship('Equipamento', backref='local', lazy=True)
    idSite = db.Column(db.Integer, db.ForeignKey('Site.id'), nullable=False)

    def __init__(self, localizadoEm='default', idSite=0):
        self.localizadoEm = localizadoEm
        self.idSite = idSite

    def __repr__(self) -> str:
        return f"Local('{self.id}, {self.localizadoEm}', '{self.idSite}')"


tipoEquipamento = db.Table(
    'tipoEquipamento',
    db.Column('idEquipamento', db.Integer, db.ForeignKey('Equipamento.id')),
    db.Column('idTipo', db.Integer, db.ForeignKey('Tipo.id'))
)


class Equipamento(db.Model):
    __tablename__ = 'Equipamento'
    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String(40), unique=True)
    patrimonio = db.Column(db.String(40), unique=True)
    hostname = db.Column(db.String(40), unique=True)
    idLocal = db.Column(db.Integer, db.ForeignKey('Local.id'), nullable=False)
    tipo = db.relationship('Tipo', secondary=tipoEquipamento, backref='tipos')

    def __init__(self, serial='S4TW02Q3', patrimonio='default', hostanme='PBR00150-XPTO', idLocal=0):
        self.serial = serial
        self.patrimonio = patrimonio
        self.hostname = hostanme
        self.idLocal = idLocal

    def __repr__(self) -> str:
        return f"Equipamento('{self.serial}', '{self.patrimonio}', '{self.hostname}')"


class Tipo(db.Model):
    __tablename__ = 'Tipo'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), unique=True, nullable=False)

    def __init__(self, nome='Anonimo'):
        self.nome = nome

    def __repr__(self):
        return f"Tipo('{self.nome}')"


class Acao(db.Model):
    __tablename__ = 'Acao'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), unique=True, nullable=False)
    relatorio = db.relationship(
        'Relatorio', backref='acaoRelatorio', lazy=True)

    def __init__(self, nome='Default') -> None:
        self.nome = nome

    def __repr__(self) -> str:
        return f"Acao('{self.nome}')"


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

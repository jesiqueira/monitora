from datetime import datetime
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
    site = db.relationship('Site', backref='endereco', lazy=True)
    funcionario = db.relationship('Funcionario', backref='endereco', lazy=True)

    def __init__(self, cidade='Default', rua='Anônima', cep='00.000-000'):
        self.rua = rua
        self.cep = cep
        self.cidade = cidade

    def __repr__(self) -> str:
        return f"Endereco('{self.cidade}', '{self.rua}', '{self.cep}')"


class Site(db.Model):
    __tablename__ = 'Site'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False, unique=True)
    idEndereco = db.Column(db.Integer, db.ForeignKey(
        'Endereco.id'), nullable=False)
    usuario = db.relationship('Usuario', backref='site', lazy=True)
    computador = db.relationship('Computador', backref='site', lazy=True)
    emprestimo = db.relationship('Emprestimo', backref='site', lazy=True)
    localpa = db.relationship('LocalPa', backref='site', lazy=True)
    localfisico = db.relationship('LocalFisico', backref='site', lazy=True)

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
    idSite = db.Column(db.Integer, db.ForeignKey('Site.id'), nullable=False)
    relatorio = db.relationship('Relatorio', backref='usuario', lazy=True)

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


class Status(db.Model):
    __tablename__ = 'Status'
    id = db.Column(db.Integer, primary_key=True)
    ativo = db.Column(db.Boolean, nullable=False, default=False)
    dataHora = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    computador = db.relationship('Computador', backref='status', lazy=True)

    def __init__(self, ativo=False, dataHora=datetime.utcnow()) -> None:
        self.ativo = ativo
        self.dataHora = dataHora

    def __repr__(self) -> str:
        return f"Status('{self.ativo}', '{self.dataHora}')"


emprestimoComputador = db.Table(
    'emprestimoComputador',
    db.Column('idEmprestimo', db.Integer, db.ForeignKey('Emprestimo.id')),
    db.Column('idComputador', db.Integer, db.ForeignKey('Computador.id'))
)

tipoComputador = db.Table(
    'tipoComputador',
    db.Column('idTipo', db.Integer, db.ForeignKey('Tipo.id')),
    db.Column('idComputador', db.Integer, db.ForeignKey('Computador.id'))
)



class Funcionario(db.Model):
    __tablename__ = 'Funcionario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), unique=True, nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    idComputador = db.Column(db.Integer, db.ForeignKey(
        'Computador.id'), nullable=False)
    idEndereco = db.Column(db.Integer, db.ForeignKey(
        'Endereco.id'), nullable=False)
    telefone = db.relationship('Telefone', backref='funcionario', lazy=True)
    emprestimo = db.relationship(
        'Emprestimo', backref='funcionario', lazy=True)

    def __init__(self, nome='XPTO', cpf='11111111111', idComputador=0, idEndereco=0) -> None:
        self.nome = nome
        self.cpf = cpf
        self.idComputador = idComputador
        self.idEndereco = idEndereco

    def __repr__(self) -> str:
        return f"Funcionario('{self.nome}', '{self.cpf}')"


class Telefone(db.Model):
    __tablename__ = 'Telefone'
    id = db.Column(db.Integer, primary_key=True)
    idFuncionario = db.Column(db.Integer, db.ForeignKey(
        'Funcionario.id'), nullable=False)
    ddd = db.Column(db.Integer, unique=True, nullable=False)
    numero = db.Column(db.Integer, unique=True, nullable=False)

    def __init__(self, ddd=000, numero=000000000, idFuncionario=0) -> None:
        self.ddd = ddd
        self.numero = numero
        self.idFuncionario = idFuncionario

    def __repr__(self) -> str:
        return f"Telefone('{self.ddd}', '{self.numero}')"


class Emprestimo(db.Model):
    __tablename__ = 'Emprestimo'
    id = db.Column(db.Integer, primary_key=True)
    dataEmprestimo = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    dataDevolucao = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Boolean, nullable=False, default=False)
    idFuncionario = db.Column(db.Integer, db.ForeignKey(
        'Funcionario.id'), nullable=False)
    idSite = db.Column(db.Integer, db.ForeignKey('Site.id'), nullable=False)
    computador = db.relationship(
        'Computador', secondary=emprestimoComputador, backref='emprestimo')

    def __init__(self, dataEmprestimo=datetime.utcnow, dataDevolucao=datetime.utcnow, status=0, idFuncionario=0, idSite=0) -> None:
        self.dataEmprestimo = dataEmprestimo
        self.dataDevolucao = dataDevolucao
        self.status = status
        self.idFuncionario = idFuncionario
        self.idSite = idSite

    def __repr__(self) -> str:
        return f"Emprestimo('{self.dataEmprestimo}', '{self.dataDevolucao}', '{self.status}')"


class Acao(db.Model):
    __tablename__ = 'Acao'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), nullable=False, unique=True)
    relatorio = db.relationship('Relatorio', backref='acao', lazy=True)

    def __init__(self, nome='XPTO') -> None:
        self.nome = nome

    def __repr__(self) -> str:
        return f"Acao('{self.nome}')"


class Relatorio(db.Model):
    __tablename__ = 'Relatorio'
    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String(40), unique=True)
    patrimonio = db.Column(db.String(40), unique=True)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    idUsuario = db.Column(db.Integer, db.ForeignKey(
        'Usuario.id'), nullable=False)
    idAcao = db.Column(db.Integer, db.ForeignKey('Acao.id'), nullable=False)

    def __init__(self, serial='XPTO', patrimonio='XPTO', data=datetime.utcnow, idUsuario=0, idAcao=0) -> None:
        self.serial = serial
        self.patrimonio = patrimonio
        self.data = data
        self.idUsuario = idUsuario
        self.idAcao = idAcao

    def __repr__(self) -> str:
        return f"Relatorio('{self.serial}', '{self.patrimonio}', '{self.data}')"


class Tipo(db.Model):
    __tablename__ = 'Tipo'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), nullable=False, unique=True)

    def __init__(self, nome='XPTO') -> None:
        self.nome = nome

    def __repr__(self) -> str:
        return f"Tipo('{self.nome}')"


class LocalPa(db.Model):
    __tablename__ = 'LocalPa'
    id = db.Column(db.Integer, primary_key=True)
    descricaoPa = db.Column(db.String(40), nullable=False, unique=True)
    idSite = db.Column(db.Integer, db.ForeignKey('Site.id'), nullable=False)
    computador = db.relationship('Computador', backref='locapa', lazy=True)

    def __init__(self, descricao='XPTO', idSite=0) -> None:
        self.descricaoPa = descricao
        self.idSite = idSite

    def __repr__(self) -> str:
        return f"LocalPa('{self.descricaoPa}')"


class LocalFisico(db.Model):
    __tablename__ = 'LocalFisico'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), nullable=False, unique=True)
    idSite = db.Column(db.Integer, db.ForeignKey('Site.id'), nullable=False)

    def __init__(self, nome='XPTO', idSite=0) -> None:
        self.nome = nome
        self.idSite = idSite

    def __repr__(self) -> str:
        return f"LocalFisico('{self.nome}')"

class Computador(db.Model):
    __tablename__ = 'Computador'
    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String(40), unique=True)
    hostname = db.Column(db.String(40), unique=True)
    patrimonio = db.Column(db.String(40), unique=True)
    idSite = db.Column(db.Integer, db.ForeignKey('Site.id'), nullable=False)
    idStatus = db.Column(db.Integer, db.ForeignKey('Status.id'), nullable=False)
    idLocalPa = db.Column(db.Integer, db.ForeignKey('LocalPa.id'), nullable=False)
    funcionario = db.relationship('Funcionario', backref='computador', lazy=True)
    tipo = db.relationship('Tipo', secondary=tipoComputador, backref='tipos')

    def __init__(self, serial='XPTO', hostname='XPTO', patrimonio='XPTO', idSite=0, idStatus=0, idlocalPa=0) -> None:
        self.serial = serial
        self.hostname = hostname
        self.patrimonio = patrimonio
        self.idSite = idSite
        self.idStatus = idStatus
        self.idLocalPa = idlocalPa

    def __repr__(self) -> str:
        return f"Computador('{self.serial}', '{self.hostname}', '{self.patrimonio}')"

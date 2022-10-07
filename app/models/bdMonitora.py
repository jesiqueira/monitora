from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


emprestimoEquipamentos = db.Table(
    'emprestimoEquipamentos',
    db.Column('idEquipamentoEmprestimo', db.Integer, db.ForeignKey('EquipamentoEmprestimos.id')),
    db.Column('idEmprestimo', db.Integer, db.ForeignKey('Emprestimos.id'))
)

userPermissoes = db.Table(
    'userPermissoes',
    db.Column('idUser', db.Integer, db.ForeignKey('Users.id')),
    db.Column('idPermissoes', db.Integer, db.ForeignKey('Permissoes.id'))
)

class Enderecos(db.Model):
    __tablename__ = 'Enderecos'
    id = db.Column(db.Integer, primary_key=True)
    rua = db.Column(db.String(40), nullable=False)
    cidade = db.Column(db.String(40), nullable=False)
    cep = db.Column(db.String(8), nullable=False)

    sites = db.relationship('Sites', backref='enderecos', lazy=True)
    funcionarios = db.relationship('Funcionarios', backref='enderecos', lazy=True)

    def __init__(self, rua='', cidade='', cep=0) -> None:
        self.rua = rua
        self.cidade = cidade
        self.cep = cep

    def __repr__(self) -> str:
        return f"Endereco(Rua: {self.rua}, Cidade: {self.cidade}, Cep: {self.cep})"


class Sites(db.Model):
    __tablename__ = 'Sites'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), nullable=False)
    idEndereco = db.Column(db.Integer, db.ForeignKey('Enderecos.id'), nullable=False)

    users = db.relationship('Users', backref='sites', lazy=True)
    pontoAtentimento = db.relationship('PontoAtendimentos', backref='sites', lazy=True)
    localizadoEm = db.relationship('LocadoEm', backref='sites', lazy=True)
    dispositivoEquipamento = db.relationship('DispositivosEquipamentos', backref='sites', lazy=True)
    emprestimos = db.relationship('Emprestimos', backref='sites', lazy=True)

    def __init__(self, nome='', idEndereco=0) -> None:
        self.nome = nome
        self.idEndereco = idEndereco

    def __repr__(self) -> str:
        return f"Sites: {self.nome}"

class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), unique=True, nullable=False)
    login = db.Column(db.String(20), unique=True, nullable=False)
    senha = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(40), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=False)
    idSite = db.Column(db.Integer, db.ForeignKey('Sites.id'), nullable=False)

    relatorios = db.relationship('Relatorios', backref='users', lazy=True)

    def __init__(self, nome='', login='', senha='', email='', ativo=1, idSite=0) -> None:
        self.nome = nome
        self.login = login
        self.senha = senha
        self.email = email
        self.ativo = ativo
        self.idSite = idSite
    
    def __repr__(self) -> str:
        return f"Users(Nome: {self.nome}, Login: {self.login}, Senha: {self.senha}, Email: {self.email}, Ativo: {self.ativo})"

class Status(db.Model):
    __tablename__ = 'Status'
    id = db.Column(db.Integer, primary_key=True)
    ativo = db.Column(db.Boolean, nullable=False, default=False)
    dataHora = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    computador = db.relationship('Computadores', backref='status', lazy=True)

    def __init__(self, ativo=1, dataHora='') -> None:
        self.ativo = ativo
        self.dataHora = dataHora
    
    def __repr__(self) -> str:
        return f"Status(Ativo: {self.ativo}, DataHora: {self.dataHora})"

class Permissoes(db.Model):
    __tablename__ = 'Permissoes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(10), unique=True, nullable=False)

    def __init__(self, nome='') -> None:
        self.nome = nome
    
    def __repr__(self) -> str:
        return f"Permissoes(Nome: {self.nome})"

class PontoAtendimentos(db.Model):
    __tablename__ = 'PontoAtendimentos'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(40), unique=True, nullable=False)
    idSite = db.Column(db.Integer, db.ForeignKey('Sites.id'), nullable=False)

    computador = db.relationship('Computadores', backref='pontoAtendimentos', lazy=True)

    def __init__(self, descricao='', idSite=0) -> None:
        self.descricao = descricao
        self.idSite = idSite
    
    def __repr__(self) -> str:
        return f"PontoAtendimentos(Descricao: {self.descricao})"

class LocadoEm(db.Model):
    __tablename__ = 'LocadoEm'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), unique=True, nullable=False)
    idSite = db.Column(db.Integer, db.ForeignKey('Sites.id'), nullable=False)

    dispositivoEquipamento = db.relationship('DispositivosEquipamentos', backref='locadoem', lazy=True)

    def __init__(self, nome='', idSite=0) -> None:
        self.nome = nome
        self.idSite = idSite

    def __repr__(self) -> str:
        return f"LocadoEm: {self.nome}"

class Tipos(db.Model):
    __tablename__ = 'Tipos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), unique=True, nullable=False)

    dispositivoEquipamento = db.relationship('DispositivosEquipamentos', backref='tipos', lazy=True)

    def __init__(self, nome='') -> None:
        self.nome = nome
    
    def __repr__(self) -> str:
        return f"Tipos: {self.nome}"

class DispositivosEquipamentos(db.Model):
    __tablename__ = 'DispositivosEquipamentos'
    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String(40), unique=True)
    hostname = db.Column(db.String(40), unique=True)
    patrimonio = db.Column(db.String(40), unique=True)
    idLocadoEm = db.Column(db.Integer, db.ForeignKey('LocadoEm.id'), nullable=False)
    idSite = db.Column(db.Integer, db.ForeignKey('Sites.id'), nullable=False)
    idTipo = db.Column(db.Integer, db.ForeignKey('Tipos.id'), nullable=False)

    computador = db.relationship('Computadores', backref='dispositivosEquipamentos', lazy=True)
    equipamentoEmprestimo = db.relationship('EquipamentoEmprestimos', backref='dispositivosEquipamentos', lazy=True)
    relatorios = db.relationship('Relatorios', backref='dispositivosEquipamentos', lazy=True)

    def __init__(self, serial='', hostname='', patrimonio='', idLocadoEm=0, idSite=0, idTipo=0) -> None:
        self.serial = serial
        self.hostname = hostname
        self.patrimonio = patrimonio
        self.idLocadoEm = idLocadoEm
        self.idSite = idSite
        self.idTipo = idTipo
    
    def __repr__(self) -> str:
        return f"DispositivosEquipamentos(Serial: {self.serial}, Hostname: {self.hostname}, Patrimonio: {self.patrimonio})"

class Computadores(db.Model):
    __tablename__ = 'Computadores'
    id = db.Column(db.Integer, primary_key=True)
    idDispositosEquipamento = db.Column(db.Integer, db.ForeignKey('DispositivosEquipamentos.id'), nullable=False)
    idPontoAtendimento = db.Column(db.Integer, db.ForeignKey('PontoAtendimentos.id'), nullable=False)
    idStatus = db.Column(db.Integer, db.ForeignKey('Status.id'), nullable=False)

    def __init__(self, idDispositosEquipamento=0, idPontoAtendimento=0, idStatus=0) -> None:
        self.idDispositosEquipamento = idDispositosEquipamento
        self.idPontoAtendimento = idPontoAtendimento
        self.idStatus = idStatus
    
    def __repr__(self) -> str:
        return f"Computador(ID_Computador: {self.idDispositoEquipamento}, ID_PontoAtendimento: {self.idPontoAtendimento}, ID_Status: {self.idStatus})"

class EquipamentoEmprestimos(db.Model):
    __tablename__ = 'EquipamentoEmprestimos'
    id = db.Column(db.Integer, primary_key=True)
    idDispositosEquipamento = db.Column(db.Integer, db.ForeignKey('DispositivosEquipamentos.id'), nullable=False)

    def __init__(self, idDispositosEquipamento=0) -> None:
        self.idDispositosEquipamento = idDispositosEquipamento
    
    def __repr__(self) -> str:
        return f"EquipamentoEmprestimos(ID_EquipamentoEmprestado: {self.idDispositosEquipamento})"

class Funcionarios(db.Model):
    __tablename__ = 'Funcionarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), unique=True, nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    idEndereco = db.Column(db.Integer, db.ForeignKey('Enderecos.id'), nullable=False)

    equipamentoEmprestimo = db.relationship('Emprestimos', backref='funcionarios', lazy=True)
    telefones = db.relationship('TelefoneFuncionarios', backref='funcionarios', lazy=True)

    def __init__(self, nome='', cpf='', idEndereco=0) -> None:
        self.nome = nome
        self.cpf = cpf
        self.idEndereco = idEndereco
    
    def __repr__(self) -> str:
        return f"Funcionarios(Nome: {self.nome}, Cpf: {self.cpf})"

class Emprestimos(db.Model):
    __tablename__ = 'Emprestimos'
    id = db.Column(db.Integer, primary_key=True)
    dataEmprestimo = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    dataDevolucao = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Boolean, nullable=False, default=False)
    idSite = db.Column(db.Integer, db.ForeignKey('Sites.id'), nullable=False)
    idFuncionario = db.Column(db.Integer, db.ForeignKey('Funcionarios.id'), nullable=False)

    def __init__(self, dataEmprestimo=datetime.utcnow, dataDevolucao=datetime.utcnow, status=False, idSite=0, idFuncionario=0) -> None:
        self.dataEmprestimo = dataEmprestimo
        self.dataDevolucao = dataDevolucao
        self.status = status
        self.idSite = idSite
        self.idFuncionario = idFuncionario
    
    def __repr__(self) -> str:
        return f"Emprestimos(DataEmprestimo: {self.dataEmprestimo}, DataDevolucao: {self.dataDevolucao}, Status: {self.status})"

class TelefoneFuncionarios(db.Model):
    __tablename__ = 'TelefoneFuncionarios'
    id = db.Column(db.Integer, primary_key=True)
    ddd = db.Column(db.String(2), nullable=False)
    numero = db.Column(db.Integer, nullable=False)
    idFuncionario = db.Column(db.Integer, db.ForeignKey('Funcionarios.id'), nullable=False)

    def __init__(self, ddd='', numero=0, idFuncionario=0) -> None:
        self.ddd = ddd
        self.numero = numero
        self.idFuncionario = idFuncionario
    
    def __repr__(self) -> str:
        return f"TelefoneFuncionarios(DDD: {self.ddd}, Numero: {self.numero})"

class Acoes(db.Model):
    __tablename__ = 'Acoes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), unique=True, nullable=False)

    relatorios = db.relationship('Relatorios', backref='acoes', lazy=True)

    def __init__(self, nome='') -> None:
        self.nome = nome
    
    def __repr__(self) -> str:
        return f"Acoes(Nome: {self.nome})"

class Relatorios(db.Model):
    __tablename__ = 'Relatorios'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    idUser = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    idDispositivosEquipamentos = db.Column(db.Integer, db.ForeignKey('DispositivosEquipamentos.id'), nullable=False)
    idAcao = db.Column(db.Integer, db.ForeignKey('Acoes.id'), nullable=False)

    def __init__(self, data=datetime.utcnow, idUser=0, idDispositovosEquipamentos=0, idAcao=0) -> None:
        self.data = data
        self.idUser = idUser
        self.idDispositivosEquipamentos = idDispositovosEquipamentos
        self.idAcao = idAcao
    
    def __repr__(self) -> str:
        return f"Relatorios(Data: {self.data})"


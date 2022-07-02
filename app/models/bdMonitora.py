from datetime import datetime
from app import db


class Endereco(db.Model):
    __tablename__ = 'Endereco'
    id = db.Column(db.Integer, primary_key=True)
    cidade = db.Column(db.String(40), nullable=False)
    rua = db.Column(db.String(40), nullable=False)
    cep = db.Column(db.String(8), nullable=False)
    sites = db.relationship('Site', backref='endereco', lazy=True)

    def __init__(self, cidade='São Paulo', rua='Anônima', cep='00.000-000'):
        self.cidade = cidade
        self.rua = rua
        self.cep = cep

    def __repr__(self) -> str:
        return f"Endereco('{self.cidade}', '{self.rua}', '{self.cep}')"


class Site(db.Model):
    __tablename__ = 'Site'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30), nullable=False)
    usuario = db.relationship('Usuario', backref='usuario', lazy=True)
    local = db.relationship('Local', backref='local', lazy=True)
    id_endereco = db.Column(db.Integer, db.ForeignKey(
        'endereco.id'), nullable=False)
    
    def __init__(self, nome='Anônio', id_endereco=0):
        self.nome = nome
        self.id_endereco = id_endereco

    def __repr__(self) -> str:
        return f"Site('{self.nome}')"


class Usuarios(db.Model):
    __tablename__ = 'Usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), unique=True, nullable=False)
    login = db.Column(db.String(20), unique=True, nullable=False)
    senha = db.Column(db.String(60), unique=True, nullable=False)
    email = db.Column(db.String(40), nullable=False)
    relatorios = db.relationship('Relatorio', backref='usuario', lazy=True)
    idSite = db.Column(db.Integer, db.Foreignkey('site.id'), nullable=False)

    def __init__(self, nome='Anonima', login='default', senha='default', email='defaul@default.com.br',idSite=0):
        self.nome = nome
        self.login = login
        self.senha = senha
        self.email = email
        self.idSite = idSite

    def __repr__(self):
        return f"Usuario('{self.nome}', '{self.login}', '{self.email}')"


class Tipo(db.Model):
    __tablename__ = 'Tipo'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), unique=True, nullable=False)
    dispositos = db.relationship('Dispositivo', backref='tipo', nullable=False)

    def __init__(self, nome='Anonimo'):
        self.nome = nome

    def __repr__(self):
        return f"Tipo('{self.nome}')"


class Local(db.Model):
    __tablename__ = 'Local'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), unique=True, nullable=False)
    dispositivo = db.relationship('Dispositivo', backref='local', lazy=True)
    relatorio = db.relationship('Relatorio', backref='localRelatorio', lazy=True)
    idSite = db.Column(db.Integer, db.ForeignKey('site.id'), nullable=False)

    def __init__(self, nome='Anonimo', dispositivo='default', idSite=0):
        self.nome = nome
        self.dispositivo = dispositivo
        self.idSite = idSite

    def __repr__(self) -> str:
        return f"Local('{self.nome}')"


class Dispositivo(db.Model):
    __tablename__ = 'Dispositivo'
    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String(40), unique=True)
    patrimonio = db.Column(db.String(40), unique=True)
    idLocal = db.Column(db.Integer, db.ForeignKey('local.id'), nullable=False)
    idTipo =db.Column(db.Integer, db.ForeignKey('tipo.id'), nullable=False)

    def __init__(self, serial='S4TW02Q3', patrimonio='default', idLocal=0, idTipo=0):
        self.serial = serial
        self.patrimonio = patrimonio
        self.idLocal = idLocal
        self.idTipo = idTipo

    def __repr__(self) -> str:
        return f"Dispositivo('{self.serial}', '{self.patrimonio}')"


class Relatorio(db.Model):
    __tablename__ = 'Relatorio'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    serial = db.Column(db.String(40), unique=True)
    patrimonio = db.Column(db.String(40), unique=True)
    idUsuario = db.Column(db.Integer, db.ForegnKey('usuario.id'), nullable=False)
    idLocal = db.Column(db.Integer, db.ForegnKey('usuario.id'), nullable=False)

    def __init__(self, data=datetime.utcnow, serial='S4TW02Q3', patrimonio='default', idUsuario=0, idLocal=0):
        self.data = data
        self.serial = serial
        self.patrimonio = patrimonio
        self.idUsuario = idUsuario

    def __repr__(self) -> str:
        return f"Relatorio('{self.data}', '{self.serial}', '{self.patrimonio}')"

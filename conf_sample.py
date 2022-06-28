import os


class Config:
    SECRET_KEY = '709bb33e1d3b513e4a9ee78a2a940063'

    
    TESTING = True
    DEBUG = True

    # DRIVER = 'postgresql'
    # USER = 'postgres'
    # PASSWORD = ''
    # HOST = 'localhost'
    # BD_HML = 'monitoraHML'
    # BD_PRD = 'monitoraPRD'

    # SQLALCHEMY_DATABASE_URI = f"{DRIVER}://{USER}:{PASSWORD}@{HOST}/{BD_HML}"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///monitora.db'
    # permite modificar bd em tempo de execução
    SQLALCHEMY_TRACK_MODIFICATIONS = True

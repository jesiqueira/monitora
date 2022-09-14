from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_login import LoginManager
from flask_migrate import Migrate, MigrateCommand
from conf import Config
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
login_manager = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    # Rotas
    from app.controllers.main.routes import main
    from app.controllers.users.routes import user
    from app.controllers.equipamento.routes import equipamento
    from app.controllers.errors.handlers import errors

    # Registrar Blueprint
    app.register_blueprint(main)
    app.register_blueprint(user)
    app.register_blueprint(equipamento)
    app.register_blueprint(errors)

    return manager

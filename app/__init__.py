from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "admin.login"
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.json.sort_keys = False

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Import models
    from . import models

    # Import blueprints
    from .admin_routes import admin_bp
    from .api.v1.api_routes import api_bp

    # Register blueprints
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(api_bp, url_prefix="/api/v1")

    return app

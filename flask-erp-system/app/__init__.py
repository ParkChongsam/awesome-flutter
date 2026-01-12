"""
Flask ERP System Application Factory
참좋은복사기 (Very Good Copy Machine) Company
"""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from flask_cors import CORS
from config import config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()


def create_app(config_name='development'):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '로그인이 필요합니다. (Login required)'
    login_manager.login_message_category = 'info'

    # User loader for Flask-Login
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from app.blueprints.auth import auth_bp
    from app.blueprints.dashboard import dashboard_bp
    from app.blueprints.inventory import inventory_bp
    from app.blueprints.sales import sales_bp
    from app.blueprints.purchasing import purchasing_bp
    from app.blueprints.service import service_bp
    from app.blueprints.accounting import accounting_bp
    from app.blueprints.hr import hr_bp
    from app.blueprints.crm import crm_bp
    from app.api import api_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(sales_bp, url_prefix='/sales')
    app.register_blueprint(purchasing_bp, url_prefix='/purchasing')
    app.register_blueprint(service_bp, url_prefix='/service')
    app.register_blueprint(accounting_bp, url_prefix='/accounting')
    app.register_blueprint(hr_bp, url_prefix='/hr')
    app.register_blueprint(crm_bp, url_prefix='/crm')
    app.register_blueprint(api_bp, url_prefix='/api')

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    # Context processors
    @app.context_processor
    def inject_company_info():
        return {
            'company_name': app.config['COMPANY_NAME'],
            'company_name_en': app.config['COMPANY_NAME_EN']
        }

    # Root route
    @app.route('/')
    def index():
        return render_template('index.html')

    return app

"""
Flask ERP System - Main Entry Point
참좋은복사기 (Very Good Copy Machine) Company
"""
import os
from app import create_app, db
from app.models import User, Role, Customer, Product, Inventory, SalesOrder, PurchaseOrder
from flask_migrate import Migrate

# Create Flask application
app = create_app(os.getenv('FLASK_ENV') or 'development')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    """Make database models available in Flask shell"""
    return {
        'db': db,
        'User': User,
        'Role': Role,
        'Customer': Customer,
        'Product': Product,
        'Inventory': Inventory,
        'SalesOrder': SalesOrder,
        'PurchaseOrder': PurchaseOrder
    }


@app.cli.command()
def init_db():
    """Initialize the database with sample data"""
    from app.utils.seed import seed_database

    print("Creating database tables...")
    db.create_all()

    print("Seeding database with initial data...")
    seed_database()

    print("Database initialized successfully!")


@app.cli.command()
def create_admin():
    """Create an admin user"""
    from getpass import getpass
    from app.models import User, Role
    from werkzeug.security import generate_password_hash

    email = input("Enter admin email: ")
    username = input("Enter admin username: ")
    password = getpass("Enter admin password: ")
    password_confirm = getpass("Confirm admin password: ")

    if password != password_confirm:
        print("Passwords do not match!")
        return

    # Get or create admin role
    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        admin_role = Role(name='admin', description='Administrator')
        db.session.add(admin_role)

    # Create admin user
    admin_user = User(
        email=email,
        username=username,
        password_hash=generate_password_hash(password),
        role=admin_role,
        is_active=True
    )

    db.session.add(admin_user)
    db.session.commit()

    print(f"Admin user '{username}' created successfully!")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

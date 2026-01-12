"""
Customer and CRM Models
"""
from datetime import datetime
from app import db


class Customer(db.Model):
    """Customer information"""
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    customer_code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    company_name = db.Column(db.String(200), nullable=False)
    business_registration = db.Column(db.String(50))

    # Contact information
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    fax = db.Column(db.String(20))
    website = db.Column(db.String(200))

    # Address
    address = db.Column(db.String(300))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100), default='South Korea')

    # Business details
    industry = db.Column(db.String(100))
    customer_type = db.Column(db.String(50))  # retail, corporate, government
    credit_limit = db.Column(db.Numeric(15, 2), default=0)
    payment_terms = db.Column(db.Integer, default=30)  # days

    # Status
    status = db.Column(db.String(20), default='active')  # active, inactive, blocked
    notes = db.Column(db.Text)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    contacts = db.relationship('CustomerContact', backref='customer', lazy='dynamic', cascade='all, delete-orphan')
    sales_orders = db.relationship('SalesOrder', backref='customer', lazy='dynamic')

    def __repr__(self):
        return f'<Customer {self.customer_code}: {self.company_name}>'


class CustomerContact(db.Model):
    """Customer contact persons"""
    __tablename__ = 'customer_contacts'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

    name = db.Column(db.String(120), nullable=False)
    position = db.Column(db.String(100))
    department = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    email = db.Column(db.String(120))

    is_primary = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<CustomerContact {self.name}>'

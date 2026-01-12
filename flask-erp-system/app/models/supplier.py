"""
Supplier and Vendor Models
"""
from datetime import datetime
from app import db


class Supplier(db.Model):
    """Supplier/Vendor information"""
    __tablename__ = 'suppliers'

    id = db.Column(db.Integer, primary_key=True)
    supplier_code = db.Column(db.String(50), unique=True, nullable=False, index=True)
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
    supplier_type = db.Column(db.String(50))  # manufacturer, distributor, service
    payment_terms = db.Column(db.Integer, default=30)  # days
    lead_time = db.Column(db.Integer, default=7)  # days

    # Banking information
    bank_name = db.Column(db.String(100))
    account_number = db.Column(db.String(50))
    account_holder = db.Column(db.String(100))

    # Status
    status = db.Column(db.String(20), default='active')  # active, inactive, blocked
    rating = db.Column(db.Integer)  # 1-5 stars
    notes = db.Column(db.Text)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    contacts = db.relationship('SupplierContact', backref='supplier', lazy='dynamic', cascade='all, delete-orphan')
    purchase_orders = db.relationship('PurchaseOrder', backref='supplier', lazy='dynamic')

    def __repr__(self):
        return f'<Supplier {self.supplier_code}: {self.company_name}>'


class SupplierContact(db.Model):
    """Supplier contact persons"""
    __tablename__ = 'supplier_contacts'

    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)

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
        return f'<SupplierContact {self.name}>'

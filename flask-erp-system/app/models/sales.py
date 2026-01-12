"""
Sales Order and Invoice Models
"""
from datetime import datetime
from app import db


class SalesOrder(db.Model):
    """Sales orders from customers"""
    __tablename__ = 'sales_orders'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    order_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)

    # Customer information
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

    # Order details
    status = db.Column(db.String(20), default='draft')  # draft, confirmed, processing, shipped, delivered, cancelled
    priority = db.Column(db.String(20), default='normal')  # low, normal, high, urgent

    # Dates
    required_date = db.Column(db.Date)
    ship_date = db.Column(db.Date)
    delivery_date = db.Column(db.Date)

    # Shipping information
    shipping_address = db.Column(db.String(300))
    shipping_city = db.Column(db.String(100))
    shipping_state = db.Column(db.String(100))
    shipping_postal_code = db.Column(db.String(20))
    shipping_method = db.Column(db.String(50))
    tracking_number = db.Column(db.String(100))

    # Financial
    subtotal = db.Column(db.Numeric(15, 2), default=0)
    discount_percent = db.Column(db.Numeric(5, 2), default=0)
    discount_amount = db.Column(db.Numeric(15, 2), default=0)
    tax_amount = db.Column(db.Numeric(15, 2), default=0)
    shipping_cost = db.Column(db.Numeric(15, 2), default=0)
    total_amount = db.Column(db.Numeric(15, 2), default=0)

    # Additional information
    payment_terms = db.Column(db.Integer, default=30)  # days
    payment_method = db.Column(db.String(50))
    notes = db.Column(db.Text)
    internal_notes = db.Column(db.Text)

    # User tracking
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    items = db.relationship('SalesOrderItem', backref='sales_order', lazy='dynamic', cascade='all, delete-orphan')
    invoices = db.relationship('Invoice', backref='sales_order', lazy='dynamic')

    def calculate_totals(self):
        """Calculate order totals"""
        self.subtotal = sum(item.line_total for item in self.items)
        self.discount_amount = self.subtotal * (self.discount_percent / 100)
        taxable_amount = self.subtotal - self.discount_amount
        self.tax_amount = taxable_amount * 0.1  # 10% VAT
        self.total_amount = taxable_amount + self.tax_amount + (self.shipping_cost or 0)

    def __repr__(self):
        return f'<SalesOrder {self.order_number}>'


class SalesOrderItem(db.Model):
    """Line items in sales orders"""
    __tablename__ = 'sales_order_items'

    id = db.Column(db.Integer, primary_key=True)
    sales_order_id = db.Column(db.Integer, db.ForeignKey('sales_orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(15, 2), nullable=False)
    discount_percent = db.Column(db.Numeric(5, 2), default=0)
    tax_rate = db.Column(db.Numeric(5, 2), default=10.0)
    line_total = db.Column(db.Numeric(15, 2), nullable=False)

    description = db.Column(db.Text)
    notes = db.Column(db.Text)

    # Relationships
    product = db.relationship('Product')

    def calculate_line_total(self):
        """Calculate line item total"""
        subtotal = self.quantity * self.unit_price
        discount = subtotal * (self.discount_percent / 100)
        self.line_total = subtotal - discount

    def __repr__(self):
        return f'<SalesOrderItem SO:{self.sales_order_id} Product:{self.product_id}>'


class Invoice(db.Model):
    """Customer invoices"""
    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    invoice_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.Date, nullable=False)

    # References
    sales_order_id = db.Column(db.Integer, db.ForeignKey('sales_orders.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

    # Financial
    subtotal = db.Column(db.Numeric(15, 2), nullable=False)
    tax_amount = db.Column(db.Numeric(15, 2), default=0)
    total_amount = db.Column(db.Numeric(15, 2), nullable=False)
    paid_amount = db.Column(db.Numeric(15, 2), default=0)
    balance = db.Column(db.Numeric(15, 2), nullable=False)

    # Status
    status = db.Column(db.String(20), default='draft')  # draft, sent, partial, paid, overdue, cancelled

    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    customer = db.relationship('Customer')
    payments = db.relationship('Payment', backref='invoice', lazy='dynamic')

    def __repr__(self):
        return f'<Invoice {self.invoice_number}>'


class Payment(db.Model):
    """Customer payments"""
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    payment_number = db.Column(db.String(50), unique=True, nullable=False)
    payment_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)

    # References
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

    # Payment details
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    payment_method = db.Column(db.String(50))  # cash, bank_transfer, credit_card, check
    reference_number = db.Column(db.String(100))

    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    customer = db.relationship('Customer')

    def __repr__(self):
        return f'<Payment {self.payment_number}>'

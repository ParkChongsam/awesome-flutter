"""
Purchase Order Models
"""
from datetime import datetime
from app import db


class PurchaseOrder(db.Model):
    """Purchase orders to suppliers"""
    __tablename__ = 'purchase_orders'

    id = db.Column(db.Integer, primary_key=True)
    po_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    po_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)

    # Supplier information
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)

    # Order details
    status = db.Column(db.String(20), default='draft')  # draft, sent, confirmed, received, cancelled
    priority = db.Column(db.String(20), default='normal')

    # Dates
    required_date = db.Column(db.Date)
    expected_date = db.Column(db.Date)
    received_date = db.Column(db.Date)

    # Delivery information
    delivery_address = db.Column(db.String(300))
    delivery_city = db.Column(db.String(100))
    delivery_contact = db.Column(db.String(100))
    delivery_phone = db.Column(db.String(20))

    # Financial
    subtotal = db.Column(db.Numeric(15, 2), default=0)
    discount_percent = db.Column(db.Numeric(5, 2), default=0)
    discount_amount = db.Column(db.Numeric(15, 2), default=0)
    tax_amount = db.Column(db.Numeric(15, 2), default=0)
    shipping_cost = db.Column(db.Numeric(15, 2), default=0)
    total_amount = db.Column(db.Numeric(15, 2), default=0)

    # Additional information
    payment_terms = db.Column(db.Integer, default=30)
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
    items = db.relationship('PurchaseOrderItem', backref='purchase_order', lazy='dynamic', cascade='all, delete-orphan')

    def calculate_totals(self):
        """Calculate order totals"""
        self.subtotal = sum(item.line_total for item in self.items)
        self.discount_amount = self.subtotal * (self.discount_percent / 100)
        taxable_amount = self.subtotal - self.discount_amount
        self.tax_amount = taxable_amount * 0.1
        self.total_amount = taxable_amount + self.tax_amount + (self.shipping_cost or 0)

    def __repr__(self):
        return f'<PurchaseOrder {self.po_number}>'


class PurchaseOrderItem(db.Model):
    """Line items in purchase orders"""
    __tablename__ = 'purchase_order_items'

    id = db.Column(db.Integer, primary_key=True)
    purchase_order_id = db.Column(db.Integer, db.ForeignKey('purchase_orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(15, 2), nullable=False)
    discount_percent = db.Column(db.Numeric(5, 2), default=0)
    tax_rate = db.Column(db.Numeric(5, 2), default=10.0)
    line_total = db.Column(db.Numeric(15, 2), nullable=False)

    quantity_received = db.Column(db.Integer, default=0)
    received_date = db.Column(db.Date)

    description = db.Column(db.Text)
    notes = db.Column(db.Text)

    # Relationships
    product = db.relationship('Product')

    def calculate_line_total(self):
        """Calculate line item total"""
        subtotal = self.quantity * self.unit_price
        discount = subtotal * (self.discount_percent / 100)
        self.line_total = subtotal - discount

    @property
    def quantity_pending(self):
        """Calculate pending quantity"""
        return self.quantity - self.quantity_received

    def __repr__(self):
        return f'<PurchaseOrderItem PO:{self.purchase_order_id} Product:{self.product_id}>'

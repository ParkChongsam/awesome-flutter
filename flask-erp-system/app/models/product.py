"""
Product and Inventory Item Models
"""
from datetime import datetime
from app import db


class ProductCategory(db.Model):
    """Product categories for organization"""
    __tablename__ = 'product_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    code = db.Column(db.String(50), unique=True)
    description = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'))

    # Self-referential relationship for hierarchical categories
    children = db.relationship('ProductCategory', backref=db.backref('parent', remote_side=[id]))
    products = db.relationship('Product', backref='category', lazy='dynamic')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ProductCategory {self.name}>'


class Product(db.Model):
    """Product/Item master data"""
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    product_code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)

    # Category and classification
    category_id = db.Column(db.Integer, db.ForeignKey('product_categories.id'))
    product_type = db.Column(db.String(50))  # copy_machine, parts, consumables, service

    # Specifications
    manufacturer = db.Column(db.String(100))
    model_number = db.Column(db.String(100))
    serial_number = db.Column(db.String(100))
    barcode = db.Column(db.String(100), unique=True)
    sku = db.Column(db.String(100), unique=True)

    # Pricing
    cost_price = db.Column(db.Numeric(15, 2), default=0)
    selling_price = db.Column(db.Numeric(15, 2), default=0)
    retail_price = db.Column(db.Numeric(15, 2), default=0)

    # Inventory
    unit_of_measure = db.Column(db.String(20), default='EA')
    reorder_level = db.Column(db.Integer, default=10)
    reorder_quantity = db.Column(db.Integer, default=50)

    # Specifications (for copy machines)
    print_speed = db.Column(db.Integer)  # pages per minute
    print_resolution = db.Column(db.String(50))
    paper_capacity = db.Column(db.Integer)
    color_support = db.Column(db.Boolean, default=False)
    duplex_support = db.Column(db.Boolean, default=False)
    network_support = db.Column(db.Boolean, default=False)

    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_taxable = db.Column(db.Boolean, default=True)
    tax_rate = db.Column(db.Numeric(5, 2), default=10.0)

    # Images and documents
    image_url = db.Column(db.String(500))
    datasheet_url = db.Column(db.String(500))

    # Notes
    notes = db.Column(db.Text)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    inventory_items = db.relationship('Inventory', backref='product', lazy='dynamic')

    @property
    def total_stock(self):
        """Calculate total stock across all warehouses"""
        return sum(inv.quantity for inv in self.inventory_items)

    @property
    def profit_margin(self):
        """Calculate profit margin percentage"""
        if self.cost_price and self.selling_price:
            return ((self.selling_price - self.cost_price) / self.cost_price) * 100
        return 0

    def __repr__(self):
        return f'<Product {self.product_code}: {self.name}>'

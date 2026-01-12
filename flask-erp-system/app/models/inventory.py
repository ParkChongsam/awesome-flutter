"""
Inventory and Warehouse Models
"""
from datetime import datetime
from app import db


class Warehouse(db.Model):
    """Warehouse/Storage location"""
    __tablename__ = 'warehouses'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(300))
    city = db.Column(db.String(100))
    manager = db.Column(db.String(100))
    phone = db.Column(db.String(20))

    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    inventory_items = db.relationship('Inventory', backref='warehouse', lazy='dynamic')

    def __repr__(self):
        return f'<Warehouse {self.code}: {self.name}>'


class Inventory(db.Model):
    """Current inventory levels by warehouse"""
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouses.id'), nullable=False)

    quantity = db.Column(db.Integer, default=0, nullable=False)
    reserved_quantity = db.Column(db.Integer, default=0)
    available_quantity = db.Column(db.Integer, default=0)

    # Location within warehouse
    location = db.Column(db.String(50))
    bin = db.Column(db.String(50))

    last_counted = db.Column(db.DateTime)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    transactions = db.relationship('InventoryTransaction', backref='inventory', lazy='dynamic')

    # Unique constraint: one product per warehouse
    __table_args__ = (db.UniqueConstraint('product_id', 'warehouse_id', name='uq_product_warehouse'),)

    def update_quantity(self, quantity_change, transaction_type, reference_id=None, notes=None):
        """Update inventory quantity and create transaction record"""
        self.quantity += quantity_change
        self.available_quantity = self.quantity - self.reserved_quantity

        # Create transaction record
        transaction = InventoryTransaction(
            inventory_id=self.id,
            transaction_type=transaction_type,
            quantity_change=quantity_change,
            quantity_after=self.quantity,
            reference_id=reference_id,
            notes=notes
        )
        db.session.add(transaction)

    def __repr__(self):
        return f'<Inventory Product:{self.product_id} Warehouse:{self.warehouse_id} Qty:{self.quantity}>'


class InventoryTransaction(db.Model):
    """Inventory movement transactions"""
    __tablename__ = 'inventory_transactions'

    id = db.Column(db.Integer, primary_key=True)
    inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'), nullable=False)

    transaction_type = db.Column(db.String(50), nullable=False)  # purchase, sale, transfer, adjustment, return
    quantity_change = db.Column(db.Integer, nullable=False)
    quantity_after = db.Column(db.Integer, nullable=False)

    reference_type = db.Column(db.String(50))  # sales_order, purchase_order, etc.
    reference_id = db.Column(db.Integer)

    cost_per_unit = db.Column(db.Numeric(15, 2))
    total_cost = db.Column(db.Numeric(15, 2))

    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<InventoryTransaction {self.transaction_type}: {self.quantity_change}>'

"""
REST API Blueprint
"""
from flask import Blueprint, jsonify, request
from flask_login import login_required
from app import db
from app.models import (
    Product, Customer, SalesOrder, PurchaseOrder,
    ServiceTicket, Inventory
)

api_bp = Blueprint('api', __name__)


# Products API
@api_bp.route('/products', methods=['GET'])
@login_required
def get_products():
    """Get all products"""
    search = request.args.get('search', '')

    query = Product.query.filter_by(is_active=True)

    if search:
        query = query.filter(
            db.or_(
                Product.product_code.ilike(f'%{search}%'),
                Product.name.ilike(f'%{search}%')
            )
        )

    products = query.all()

    return jsonify([{
        'id': p.id,
        'product_code': p.product_code,
        'name': p.name,
        'selling_price': float(p.selling_price) if p.selling_price else 0,
        'stock': p.total_stock
    } for p in products])


@api_bp.route('/products/<int:product_id>', methods=['GET'])
@login_required
def get_product(product_id):
    """Get single product"""
    product = Product.query.get_or_404(product_id)

    return jsonify({
        'id': product.id,
        'product_code': product.product_code,
        'name': product.name,
        'description': product.description,
        'cost_price': float(product.cost_price) if product.cost_price else 0,
        'selling_price': float(product.selling_price) if product.selling_price else 0,
        'stock': product.total_stock
    })


# Customers API
@api_bp.route('/customers', methods=['GET'])
@login_required
def get_customers():
    """Get all customers"""
    search = request.args.get('search', '')

    query = Customer.query.filter_by(status='active')

    if search:
        query = query.filter(
            db.or_(
                Customer.customer_code.ilike(f'%{search}%'),
                Customer.company_name.ilike(f'%{search}%')
            )
        )

    customers = query.all()

    return jsonify([{
        'id': c.id,
        'customer_code': c.customer_code,
        'company_name': c.company_name,
        'phone': c.phone,
        'email': c.email
    } for c in customers])


@api_bp.route('/customers/<int:customer_id>', methods=['GET'])
@login_required
def get_customer(customer_id):
    """Get single customer"""
    customer = Customer.query.get_or_404(customer_id)

    return jsonify({
        'id': customer.id,
        'customer_code': customer.customer_code,
        'company_name': customer.company_name,
        'phone': customer.phone,
        'email': customer.email,
        'address': customer.address,
        'credit_limit': float(customer.credit_limit) if customer.credit_limit else 0
    })


# Sales Orders API
@api_bp.route('/sales-orders', methods=['GET'])
@login_required
def get_sales_orders():
    """Get all sales orders"""
    status = request.args.get('status', '')

    query = SalesOrder.query

    if status:
        query = query.filter_by(status=status)

    orders = query.order_by(SalesOrder.order_date.desc()).limit(100).all()

    return jsonify([{
        'id': o.id,
        'order_number': o.order_number,
        'order_date': o.order_date.isoformat() if o.order_date else None,
        'customer_id': o.customer_id,
        'customer_name': o.customer.company_name if o.customer else None,
        'status': o.status,
        'total_amount': float(o.total_amount) if o.total_amount else 0
    } for o in orders])


# Inventory API
@api_bp.route('/inventory', methods=['GET'])
@login_required
def get_inventory():
    """Get inventory levels"""
    inventory_items = Inventory.query.join(Product).all()

    return jsonify([{
        'product_id': i.product_id,
        'product_code': i.product.product_code,
        'product_name': i.product.name,
        'warehouse_id': i.warehouse_id,
        'quantity': i.quantity,
        'available_quantity': i.available_quantity
    } for i in inventory_items])


# Health check
@api_bp.route('/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({'status': 'healthy', 'message': 'API is running'})

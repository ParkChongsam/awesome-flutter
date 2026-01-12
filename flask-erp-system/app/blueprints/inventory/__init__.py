"""
Inventory Management Blueprint
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Product, ProductCategory, Inventory, Warehouse, InventoryTransaction
from sqlalchemy import func

inventory_bp = Blueprint('inventory', __name__, template_folder='../../templates/inventory')


@inventory_bp.route('/')
@login_required
def index():
    """Inventory list"""
    page = request.args.get('page', 1, type=int)
    per_page = 20

    # Get products with inventory levels
    products = Product.query.filter_by(is_active=True).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return render_template('index.html', products=products)


@inventory_bp.route('/products')
@login_required
def products():
    """Product list"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    category_id = request.args.get('category', type=int)

    query = Product.query

    if search:
        query = query.filter(
            db.or_(
                Product.product_code.ilike(f'%{search}%'),
                Product.name.ilike(f'%{search}%'),
                Product.description.ilike(f'%{search}%')
            )
        )

    if category_id:
        query = query.filter_by(category_id=category_id)

    products = query.order_by(Product.product_code).paginate(
        page=page, per_page=20, error_out=False
    )

    categories = ProductCategory.query.all()

    return render_template('products.html', products=products, categories=categories)


@inventory_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    """Add new product"""
    if request.method == 'POST':
        product = Product(
            product_code=request.form.get('product_code'),
            name=request.form.get('name'),
            description=request.form.get('description'),
            category_id=request.form.get('category_id') or None,
            product_type=request.form.get('product_type'),
            manufacturer=request.form.get('manufacturer'),
            model_number=request.form.get('model_number'),
            cost_price=request.form.get('cost_price'),
            selling_price=request.form.get('selling_price'),
            retail_price=request.form.get('retail_price'),
            unit_of_measure=request.form.get('unit_of_measure', 'EA'),
            reorder_level=request.form.get('reorder_level', 10),
            reorder_quantity=request.form.get('reorder_quantity', 50)
        )

        db.session.add(product)
        db.session.commit()

        flash('제품이 추가되었습니다. (Product added successfully)', 'success')
        return redirect(url_for('inventory.products'))

    categories = ProductCategory.query.all()
    return render_template('add_product.html', categories=categories)


@inventory_bp.route('/products/<int:product_id>')
@login_required
def product_detail(product_id):
    """Product detail page"""
    product = Product.query.get_or_404(product_id)
    inventory_items = Inventory.query.filter_by(product_id=product_id).all()

    return render_template('product_detail.html', product=product, inventory_items=inventory_items)


@inventory_bp.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    """Edit product"""
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.category_id = request.form.get('category_id') or None
        product.manufacturer = request.form.get('manufacturer')
        product.cost_price = request.form.get('cost_price')
        product.selling_price = request.form.get('selling_price')
        product.retail_price = request.form.get('retail_price')

        db.session.commit()

        flash('제품이 수정되었습니다. (Product updated successfully)', 'success')
        return redirect(url_for('inventory.product_detail', product_id=product_id))

    categories = ProductCategory.query.all()
    return render_template('edit_product.html', product=product, categories=categories)


@inventory_bp.route('/warehouses')
@login_required
def warehouses():
    """Warehouse list"""
    warehouses = Warehouse.query.filter_by(is_active=True).all()
    return render_template('warehouses.html', warehouses=warehouses)


@inventory_bp.route('/adjust', methods=['GET', 'POST'])
@login_required
def adjust_inventory():
    """Adjust inventory levels"""
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        warehouse_id = request.form.get('warehouse_id')
        quantity_change = int(request.form.get('quantity_change'))
        notes = request.form.get('notes')

        inventory = Inventory.query.filter_by(
            product_id=product_id,
            warehouse_id=warehouse_id
        ).first()

        if not inventory:
            inventory = Inventory(
                product_id=product_id,
                warehouse_id=warehouse_id,
                quantity=0
            )
            db.session.add(inventory)

        inventory.update_quantity(
            quantity_change=quantity_change,
            transaction_type='adjustment',
            notes=notes
        )

        db.session.commit()

        flash('재고가 조정되었습니다. (Inventory adjusted successfully)', 'success')
        return redirect(url_for('inventory.index'))

    products = Product.query.filter_by(is_active=True).all()
    warehouses = Warehouse.query.filter_by(is_active=True).all()

    return render_template('adjust_inventory.html', products=products, warehouses=warehouses)


@inventory_bp.route('/transactions')
@login_required
def transactions():
    """Inventory transaction history"""
    page = request.args.get('page', 1, type=int)

    transactions = InventoryTransaction.query.order_by(
        InventoryTransaction.created_at.desc()
    ).paginate(page=page, per_page=50, error_out=False)

    return render_template('transactions.html', transactions=transactions)


@inventory_bp.route('/categories')
@login_required
def categories():
    """Product categories"""
    categories = ProductCategory.query.all()
    return render_template('categories.html', categories=categories)

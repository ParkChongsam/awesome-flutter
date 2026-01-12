"""
Purchasing Management Blueprint
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import PurchaseOrder, PurchaseOrderItem, Supplier, Product
from datetime import datetime

purchasing_bp = Blueprint('purchasing', __name__, template_folder='../../templates/purchasing')


@purchasing_bp.route('/')
@login_required
def index():
    """Purchase orders list"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')

    query = PurchaseOrder.query

    if status:
        query = query.filter_by(status=status)

    orders = query.order_by(PurchaseOrder.po_date.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('index.html', orders=orders, current_status=status)


@purchasing_bp.route('/orders/new', methods=['GET', 'POST'])
@login_required
def new_order():
    """Create new purchase order"""
    if request.method == 'POST':
        order = PurchaseOrder(
            po_number=f"PO-{datetime.utcnow().strftime('%Y%m%d')}-{PurchaseOrder.query.count() + 1:04d}",
            po_date=datetime.utcnow().date(),
            supplier_id=request.form.get('supplier_id'),
            status='draft',
            created_by=current_user.id
        )

        db.session.add(order)
        db.session.commit()

        flash('구매 주문이 생성되었습니다. (Purchase order created successfully)', 'success')
        return redirect(url_for('purchasing.order_detail', order_id=order.id))

    suppliers = Supplier.query.filter_by(status='active').order_by(Supplier.company_name).all()
    products = Product.query.filter_by(is_active=True).order_by(Product.name).all()

    return render_template('new_order.html', suppliers=suppliers, products=products)


@purchasing_bp.route('/orders/<int:order_id>')
@login_required
def order_detail(order_id):
    """Purchase order detail"""
    order = PurchaseOrder.query.get_or_404(order_id)
    return render_template('order_detail.html', order=order)


@purchasing_bp.route('/orders/<int:order_id>/receive', methods=['GET', 'POST'])
@login_required
def receive_order(order_id):
    """Receive purchase order items"""
    order = PurchaseOrder.query.get_or_404(order_id)

    if request.method == 'POST':
        # Process received items
        # Update inventory
        order.status = 'received'
        order.received_date = datetime.utcnow().date()
        db.session.commit()

        flash('구매 주문이 입고 처리되었습니다. (Purchase order received successfully)', 'success')
        return redirect(url_for('purchasing.order_detail', order_id=order_id))

    return render_template('receive_order.html', order=order)


@purchasing_bp.route('/suppliers')
@login_required
def suppliers():
    """Suppliers list"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')

    query = Supplier.query

    if search:
        query = query.filter(
            db.or_(
                Supplier.supplier_code.ilike(f'%{search}%'),
                Supplier.company_name.ilike(f'%{search}%')
            )
        )

    suppliers = query.order_by(Supplier.company_name).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('suppliers.html', suppliers=suppliers)


@purchasing_bp.route('/suppliers/<int:supplier_id>')
@login_required
def supplier_detail(supplier_id):
    """Supplier detail"""
    supplier = Supplier.query.get_or_404(supplier_id)
    orders = PurchaseOrder.query.filter_by(supplier_id=supplier_id).order_by(
        PurchaseOrder.po_date.desc()
    ).limit(10).all()

    return render_template('supplier_detail.html', supplier=supplier, orders=orders)

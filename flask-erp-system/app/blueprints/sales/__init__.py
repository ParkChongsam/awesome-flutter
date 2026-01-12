"""
Sales Management Blueprint
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import SalesOrder, SalesOrderItem, Customer, Product, Invoice, Payment
from datetime import datetime

sales_bp = Blueprint('sales', __name__, template_folder='../../templates/sales')


@sales_bp.route('/')
@login_required
def index():
    """Sales orders list"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')

    query = SalesOrder.query

    if status:
        query = query.filter_by(status=status)

    orders = query.order_by(SalesOrder.order_date.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('index.html', orders=orders, current_status=status)


@sales_bp.route('/orders/new', methods=['GET', 'POST'])
@login_required
def new_order():
    """Create new sales order"""
    if request.method == 'POST':
        order = SalesOrder(
            order_number=f"SO-{datetime.utcnow().strftime('%Y%m%d')}-{SalesOrder.query.count() + 1:04d}",
            order_date=datetime.utcnow().date(),
            customer_id=request.form.get('customer_id'),
            status='draft',
            created_by=current_user.id
        )

        db.session.add(order)
        db.session.flush()  # Get the order ID

        # Add order items (would typically come from a form array)
        # This is a simplified version
        flash('판매 주문이 생성되었습니다. (Sales order created successfully)', 'success')
        return redirect(url_for('sales.order_detail', order_id=order.id))

    customers = Customer.query.filter_by(status='active').order_by(Customer.company_name).all()
    products = Product.query.filter_by(is_active=True).order_by(Product.name).all()

    return render_template('new_order.html', customers=customers, products=products)


@sales_bp.route('/orders/<int:order_id>')
@login_required
def order_detail(order_id):
    """Sales order detail"""
    order = SalesOrder.query.get_or_404(order_id)
    return render_template('order_detail.html', order=order)


@sales_bp.route('/orders/<int:order_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_order(order_id):
    """Edit sales order"""
    order = SalesOrder.query.get_or_404(order_id)

    if order.status not in ['draft', 'confirmed']:
        flash('이 주문은 수정할 수 없습니다. (This order cannot be edited)', 'warning')
        return redirect(url_for('sales.order_detail', order_id=order_id))

    if request.method == 'POST':
        order.required_date = request.form.get('required_date')
        order.shipping_address = request.form.get('shipping_address')
        order.notes = request.form.get('notes')

        db.session.commit()

        flash('주문이 수정되었습니다. (Order updated successfully)', 'success')
        return redirect(url_for('sales.order_detail', order_id=order_id))

    return render_template('edit_order.html', order=order)


@sales_bp.route('/orders/<int:order_id>/confirm', methods=['POST'])
@login_required
def confirm_order(order_id):
    """Confirm sales order"""
    order = SalesOrder.query.get_or_404(order_id)

    if order.status != 'draft':
        flash('이 주문은 이미 확정되었습니다. (This order is already confirmed)', 'warning')
        return redirect(url_for('sales.order_detail', order_id=order_id))

    order.status = 'confirmed'
    order.approved_by = current_user.id
    db.session.commit()

    flash('주문이 확정되었습니다. (Order confirmed successfully)', 'success')
    return redirect(url_for('sales.order_detail', order_id=order_id))


@sales_bp.route('/invoices')
@login_required
def invoices():
    """Invoices list"""
    page = request.args.get('page', 1, type=int)

    invoices = Invoice.query.order_by(Invoice.invoice_date.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('invoices.html', invoices=invoices)


@sales_bp.route('/invoices/<int:invoice_id>')
@login_required
def invoice_detail(invoice_id):
    """Invoice detail"""
    invoice = Invoice.query.get_or_404(invoice_id)
    return render_template('invoice_detail.html', invoice=invoice)


@sales_bp.route('/payments')
@login_required
def payments():
    """Payments list"""
    page = request.args.get('page', 1, type=int)

    payments = Payment.query.order_by(Payment.payment_date.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('payments.html', payments=payments)


@sales_bp.route('/customers')
@login_required
def customers():
    """Customers list"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')

    query = Customer.query

    if search:
        query = query.filter(
            db.or_(
                Customer.customer_code.ilike(f'%{search}%'),
                Customer.company_name.ilike(f'%{search}%')
            )
        )

    customers = query.order_by(Customer.company_name).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('customers.html', customers=customers)


@sales_bp.route('/customers/<int:customer_id>')
@login_required
def customer_detail(customer_id):
    """Customer detail"""
    customer = Customer.query.get_or_404(customer_id)
    orders = SalesOrder.query.filter_by(customer_id=customer_id).order_by(
        SalesOrder.order_date.desc()
    ).limit(10).all()

    return render_template('customer_detail.html', customer=customer, orders=orders)


@sales_bp.route('/reports/sales-summary')
@login_required
def sales_summary():
    """Sales summary report"""
    return render_template('sales_summary.html')

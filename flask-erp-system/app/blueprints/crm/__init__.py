"""
Customer Relationship Management Blueprint
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Customer, CustomerContact, SalesOrder, ServiceTicket

crm_bp = Blueprint('crm', __name__, template_folder='../../templates/crm')


@crm_bp.route('/')
@login_required
def index():
    """CRM dashboard"""
    total_customers = Customer.query.filter_by(status='active').count()
    return render_template('index.html', total_customers=total_customers)


@crm_bp.route('/customers')
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


@crm_bp.route('/customers/new', methods=['GET', 'POST'])
@login_required
def new_customer():
    """Create new customer"""
    if request.method == 'POST':
        customer = Customer(
            customer_code=request.form.get('customer_code'),
            company_name=request.form.get('company_name'),
            phone=request.form.get('phone'),
            email=request.form.get('email'),
            address=request.form.get('address'),
            city=request.form.get('city'),
            customer_type=request.form.get('customer_type', 'corporate')
        )

        db.session.add(customer)
        db.session.commit()

        flash('고객이 추가되었습니다. (Customer added successfully)', 'success')
        return redirect(url_for('crm.customer_detail', customer_id=customer.id))

    return render_template('new_customer.html')


@crm_bp.route('/customers/<int:customer_id>')
@login_required
def customer_detail(customer_id):
    """Customer detail"""
    customer = Customer.query.get_or_404(customer_id)
    orders = SalesOrder.query.filter_by(customer_id=customer_id).order_by(
        SalesOrder.order_date.desc()
    ).limit(10).all()
    tickets = ServiceTicket.query.filter_by(customer_id=customer_id).order_by(
        ServiceTicket.ticket_date.desc()
    ).limit(10).all()

    return render_template('customer_detail.html', customer=customer, orders=orders, tickets=tickets)


@crm_bp.route('/customers/<int:customer_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_customer(customer_id):
    """Edit customer"""
    customer = Customer.query.get_or_404(customer_id)

    if request.method == 'POST':
        customer.company_name = request.form.get('company_name')
        customer.phone = request.form.get('phone')
        customer.email = request.form.get('email')
        customer.address = request.form.get('address')

        db.session.commit()

        flash('고객 정보가 수정되었습니다. (Customer updated successfully)', 'success')
        return redirect(url_for('crm.customer_detail', customer_id=customer_id))

    return render_template('edit_customer.html', customer=customer)

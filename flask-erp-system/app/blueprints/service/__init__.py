"""
Service Management Blueprint
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import ServiceTicket, Technician, Customer, Product, ServiceSchedule
from datetime import datetime

service_bp = Blueprint('service', __name__, template_folder='../../templates/service')


@service_bp.route('/')
@login_required
def index():
    """Service tickets list"""
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')

    query = ServiceTicket.query

    if status:
        query = query.filter_by(status=status)

    tickets = query.order_by(ServiceTicket.ticket_date.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('index.html', tickets=tickets, current_status=status)


@service_bp.route('/tickets/new', methods=['GET', 'POST'])
@login_required
def new_ticket():
    """Create new service ticket"""
    if request.method == 'POST':
        ticket = ServiceTicket(
            ticket_number=f"ST-{datetime.utcnow().strftime('%Y%m%d')}-{ServiceTicket.query.count() + 1:04d}",
            ticket_date=datetime.utcnow(),
            customer_id=request.form.get('customer_id'),
            product_id=request.form.get('product_id') or None,
            service_type=request.form.get('service_type'),
            priority=request.form.get('priority', 'normal'),
            problem_description=request.form.get('problem_description'),
            service_location=request.form.get('service_location'),
            created_by=current_user.id
        )

        db.session.add(ticket)
        db.session.commit()

        flash('서비스 티켓이 생성되었습니다. (Service ticket created successfully)', 'success')
        return redirect(url_for('service.ticket_detail', ticket_id=ticket.id))

    customers = Customer.query.filter_by(status='active').order_by(Customer.company_name).all()
    products = Product.query.filter_by(is_active=True).order_by(Product.name).all()
    technicians = Technician.query.filter_by(is_active=True).all()

    return render_template('new_ticket.html', customers=customers, products=products, technicians=technicians)


@service_bp.route('/tickets/<int:ticket_id>')
@login_required
def ticket_detail(ticket_id):
    """Service ticket detail"""
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    return render_template('ticket_detail.html', ticket=ticket)


@service_bp.route('/tickets/<int:ticket_id>/assign', methods=['POST'])
@login_required
def assign_ticket(ticket_id):
    """Assign ticket to technician"""
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    technician_id = request.form.get('technician_id')

    ticket.technician_id = technician_id
    ticket.status = 'assigned'

    db.session.commit()

    flash('티켓이 배정되었습니다. (Ticket assigned successfully)', 'success')
    return redirect(url_for('service.ticket_detail', ticket_id=ticket_id))


@service_bp.route('/tickets/<int:ticket_id>/complete', methods=['POST'])
@login_required
def complete_ticket(ticket_id):
    """Complete service ticket"""
    ticket = ServiceTicket.query.get_or_404(ticket_id)

    ticket.status = 'completed'
    ticket.completion_time = datetime.utcnow()
    ticket.solution = request.form.get('solution')
    ticket.actual_hours = request.form.get('actual_hours')

    ticket.calculate_total_cost()

    db.session.commit()

    flash('서비스가 완료되었습니다. (Service completed successfully)', 'success')
    return redirect(url_for('service.ticket_detail', ticket_id=ticket_id))


@service_bp.route('/technicians')
@login_required
def technicians():
    """Technicians list"""
    technicians = Technician.query.filter_by(is_active=True).all()
    return render_template('technicians.html', technicians=technicians)


@service_bp.route('/schedule')
@login_required
def schedule():
    """Service schedule"""
    date = request.args.get('date', datetime.utcnow().date())

    schedules = ServiceSchedule.query.filter_by(schedule_date=date).all()

    return render_template('schedule.html', schedules=schedules, date=date)

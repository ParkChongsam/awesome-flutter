"""
Human Resources Blueprint
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Employee, Department, Attendance, Payroll

hr_bp = Blueprint('hr', __name__, template_folder='../../templates/hr')


@hr_bp.route('/')
@login_required
def index():
    """HR dashboard"""
    total_employees = Employee.query.filter_by(status='active').count()
    departments = Department.query.filter_by(is_active=True).all()

    return render_template('index.html', total_employees=total_employees, departments=departments)


@hr_bp.route('/employees')
@login_required
def employees():
    """Employees list"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')

    query = Employee.query.filter_by(status='active')

    if search:
        query = query.filter(
            db.or_(
                Employee.employee_code.ilike(f'%{search}%'),
                Employee.full_name.ilike(f'%{search}%')
            )
        )

    employees = query.order_by(Employee.employee_code).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('employees.html', employees=employees)


@hr_bp.route('/employees/<int:employee_id>')
@login_required
def employee_detail(employee_id):
    """Employee detail"""
    employee = Employee.query.get_or_404(employee_id)
    return render_template('employee_detail.html', employee=employee)


@hr_bp.route('/attendance')
@login_required
def attendance():
    """Attendance tracking"""
    date = request.args.get('date', datetime.utcnow().date())

    attendance_records = Attendance.query.filter_by(date=date).all()

    return render_template('attendance.html', attendance_records=attendance_records, date=date)


@hr_bp.route('/payroll')
@login_required
def payroll():
    """Payroll management"""
    page = request.args.get('page', 1, type=int)

    payroll_records = Payroll.query.order_by(Payroll.pay_date.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('payroll.html', payroll_records=payroll_records)


@hr_bp.route('/departments')
@login_required
def departments():
    """Departments list"""
    departments = Department.query.filter_by(is_active=True).all()
    return render_template('departments.html', departments=departments)

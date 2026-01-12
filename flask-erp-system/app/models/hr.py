"""
Human Resources Models
"""
from datetime import datetime
from app import db


class Department(db.Model):
    """Company departments"""
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    # Hierarchy
    parent_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    manager_id = db.Column(db.Integer, db.ForeignKey('employees.id'))

    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    children = db.relationship('Department', backref=db.backref('parent', remote_side=[id]))
    employees = db.relationship('Employee', foreign_keys='Employee.department_id', backref='department', lazy='dynamic')

    def __repr__(self):
        return f'<Department {self.code}: {self.name}>'


class Employee(db.Model):
    """Employee information"""
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    employee_code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Personal information
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    national_id = db.Column(db.String(50))

    # Contact information
    phone = db.Column(db.String(20))
    mobile = db.Column(db.String(20))
    email = db.Column(db.String(120))
    personal_email = db.Column(db.String(120))

    # Address
    address = db.Column(db.String(300))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))

    # Employment details
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    position = db.Column(db.String(100))
    job_title = db.Column(db.String(100))
    employment_type = db.Column(db.String(50))  # full_time, part_time, contract, intern

    # Dates
    hire_date = db.Column(db.Date, nullable=False)
    probation_end_date = db.Column(db.Date)
    termination_date = db.Column(db.Date)

    # Manager
    manager_id = db.Column(db.Integer, db.ForeignKey('employees.id'))

    # Compensation
    salary = db.Column(db.Numeric(15, 2))
    salary_currency = db.Column(db.String(3), default='KRW')
    pay_frequency = db.Column(db.String(20))  # monthly, bi_weekly, weekly

    # Banking
    bank_name = db.Column(db.String(100))
    account_number = db.Column(db.String(50))
    account_holder = db.Column(db.String(100))

    # Emergency contact
    emergency_contact_name = db.Column(db.String(120))
    emergency_contact_phone = db.Column(db.String(20))
    emergency_contact_relationship = db.Column(db.String(50))

    # Status
    status = db.Column(db.String(20), default='active')  # active, on_leave, terminated
    is_active = db.Column(db.Boolean, default=True)

    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref='employee')
    manager = db.relationship('Employee', remote_side=[id], backref='subordinates')
    attendance_records = db.relationship('Attendance', backref='employee', lazy='dynamic')
    payroll_records = db.relationship('Payroll', backref='employee', lazy='dynamic')
    managed_departments = db.relationship('Department', foreign_keys=[Department.manager_id], backref='manager')

    @property
    def age(self):
        """Calculate employee age"""
        if self.date_of_birth:
            today = datetime.utcnow().date()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

    def __repr__(self):
        return f'<Employee {self.employee_code}: {self.full_name}>'


class Attendance(db.Model):
    """Employee attendance records"""
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)

    date = db.Column(db.Date, nullable=False, index=True)
    clock_in = db.Column(db.Time)
    clock_out = db.Column(db.Time)

    status = db.Column(db.String(20), default='present')  # present, absent, late, half_day, on_leave
    attendance_type = db.Column(db.String(50))  # regular, overtime, holiday, weekend

    # Hours
    regular_hours = db.Column(db.Numeric(5, 2), default=0)
    overtime_hours = db.Column(db.Numeric(5, 2), default=0)
    total_hours = db.Column(db.Numeric(5, 2), default=0)

    # Leave
    leave_type = db.Column(db.String(50))  # annual, sick, unpaid, maternity, etc.
    is_approved = db.Column(db.Boolean)

    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Unique constraint
    __table_args__ = (db.UniqueConstraint('employee_id', 'date', name='uq_employee_date'),)

    def calculate_hours(self):
        """Calculate work hours"""
        if self.clock_in and self.clock_out:
            clock_in_dt = datetime.combine(datetime.today(), self.clock_in)
            clock_out_dt = datetime.combine(datetime.today(), self.clock_out)
            duration = clock_out_dt - clock_in_dt
            self.total_hours = duration.total_seconds() / 3600

            # Calculate regular vs overtime (assuming 8 hour work day)
            if self.total_hours <= 8:
                self.regular_hours = self.total_hours
                self.overtime_hours = 0
            else:
                self.regular_hours = 8
                self.overtime_hours = self.total_hours - 8

    def __repr__(self):
        return f'<Attendance Employee:{self.employee_id} Date:{self.date}>'


class Payroll(db.Model):
    """Employee payroll records"""
    __tablename__ = 'payroll'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)

    pay_period_start = db.Column(db.Date, nullable=False)
    pay_period_end = db.Column(db.Date, nullable=False)
    pay_date = db.Column(db.Date, nullable=False)

    # Earnings
    basic_salary = db.Column(db.Numeric(15, 2), default=0)
    overtime_pay = db.Column(db.Numeric(15, 2), default=0)
    allowances = db.Column(db.Numeric(15, 2), default=0)
    bonus = db.Column(db.Numeric(15, 2), default=0)
    gross_pay = db.Column(db.Numeric(15, 2), default=0)

    # Deductions
    tax_deduction = db.Column(db.Numeric(15, 2), default=0)
    insurance_deduction = db.Column(db.Numeric(15, 2), default=0)
    pension_deduction = db.Column(db.Numeric(15, 2), default=0)
    other_deductions = db.Column(db.Numeric(15, 2), default=0)
    total_deductions = db.Column(db.Numeric(15, 2), default=0)

    # Net pay
    net_pay = db.Column(db.Numeric(15, 2), default=0)

    # Payment details
    payment_method = db.Column(db.String(50))  # bank_transfer, cash, check
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, cancelled
    payment_reference = db.Column(db.String(100))

    notes = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def calculate_net_pay(self):
        """Calculate net pay"""
        self.gross_pay = (self.basic_salary or 0) + (self.overtime_pay or 0) + (self.allowances or 0) + (self.bonus or 0)
        self.total_deductions = (self.tax_deduction or 0) + (self.insurance_deduction or 0) + (self.pension_deduction or 0) + (self.other_deductions or 0)
        self.net_pay = self.gross_pay - self.total_deductions

    def __repr__(self):
        return f'<Payroll Employee:{self.employee_id} Period:{self.pay_period_start}-{self.pay_period_end}>'

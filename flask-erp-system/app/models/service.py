"""
Service and Maintenance Models
"""
from datetime import datetime
from app import db


class Technician(db.Model):
    """Service technicians"""
    __tablename__ = 'technicians'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    technician_code = db.Column(db.String(50), unique=True, nullable=False)

    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))

    # Skills and certifications
    specialization = db.Column(db.String(200))
    certifications = db.Column(db.Text)
    skill_level = db.Column(db.String(20))  # junior, intermediate, senior, expert

    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    service_tickets = db.relationship('ServiceTicket', backref='technician', lazy='dynamic')
    schedules = db.relationship('ServiceSchedule', backref='technician', lazy='dynamic')

    def __repr__(self):
        return f'<Technician {self.technician_code}: {self.name}>'


class ServiceTicket(db.Model):
    """Service tickets for maintenance and repairs"""
    __tablename__ = 'service_tickets'

    id = db.Column(db.Integer, primary_key=True)
    ticket_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    ticket_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Customer and equipment
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))  # Equipment being serviced
    serial_number = db.Column(db.String(100))

    # Service details
    service_type = db.Column(db.String(50))  # installation, maintenance, repair, inspection
    priority = db.Column(db.String(20), default='normal')  # low, normal, high, urgent
    status = db.Column(db.String(20), default='open')  # open, assigned, in_progress, completed, cancelled

    # Problem description
    problem_description = db.Column(db.Text, nullable=False)
    diagnosis = db.Column(db.Text)
    solution = db.Column(db.Text)

    # Assignment
    technician_id = db.Column(db.Integer, db.ForeignKey('technicians.id'))

    # Scheduling
    scheduled_date = db.Column(db.DateTime)
    start_time = db.Column(db.DateTime)
    completion_time = db.Column(db.DateTime)

    # Location
    service_location = db.Column(db.String(300))
    customer_contact = db.Column(db.String(100))
    contact_phone = db.Column(db.String(20))

    # Parts and costs
    parts_cost = db.Column(db.Numeric(15, 2), default=0)
    labor_cost = db.Column(db.Numeric(15, 2), default=0)
    travel_cost = db.Column(db.Numeric(15, 2), default=0)
    total_cost = db.Column(db.Numeric(15, 2), default=0)

    # Hours
    estimated_hours = db.Column(db.Numeric(5, 2))
    actual_hours = db.Column(db.Numeric(5, 2))

    # Warranty
    is_under_warranty = db.Column(db.Boolean, default=False)
    warranty_claim_number = db.Column(db.String(50))

    # Customer feedback
    customer_rating = db.Column(db.Integer)  # 1-5 stars
    customer_feedback = db.Column(db.Text)

    notes = db.Column(db.Text)
    internal_notes = db.Column(db.Text)

    # User tracking
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    customer = db.relationship('Customer')
    product = db.relationship('Product')

    def calculate_total_cost(self):
        """Calculate total service cost"""
        self.total_cost = (self.parts_cost or 0) + (self.labor_cost or 0) + (self.travel_cost or 0)

    def __repr__(self):
        return f'<ServiceTicket {self.ticket_number}>'


class ServiceSchedule(db.Model):
    """Scheduled maintenance and service appointments"""
    __tablename__ = 'service_schedules'

    id = db.Column(db.Integer, primary_key=True)
    schedule_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime)

    # Assignment
    technician_id = db.Column(db.Integer, db.ForeignKey('technicians.id'), nullable=False)
    service_ticket_id = db.Column(db.Integer, db.ForeignKey('service_tickets.id'))

    # Customer information
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    customer_name = db.Column(db.String(200))
    customer_address = db.Column(db.String(300))
    customer_phone = db.Column(db.String(20))

    # Schedule details
    service_type = db.Column(db.String(50))
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, in_progress, completed, cancelled

    # Reminder
    send_reminder = db.Column(db.Boolean, default=True)
    reminder_sent = db.Column(db.Boolean, default=False)

    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    customer = db.relationship('Customer')
    service_ticket = db.relationship('ServiceTicket')

    def __repr__(self):
        return f'<ServiceSchedule {self.id} on {self.schedule_date}>'

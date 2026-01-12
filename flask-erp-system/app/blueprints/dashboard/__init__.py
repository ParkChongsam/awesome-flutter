"""
Dashboard Blueprint
"""
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app import db
from app.models import (
    Customer, Product, SalesOrder, PurchaseOrder,
    ServiceTicket, Invoice, Inventory
)
from sqlalchemy import func
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__, template_folder='../../templates/dashboard')


@dashboard_bp.route('/')
@login_required
def index():
    """Main dashboard page"""

    # Get statistics
    stats = {
        'total_customers': Customer.query.filter_by(status='active').count(),
        'total_products': Product.query.filter_by(is_active=True).count(),
        'pending_orders': SalesOrder.query.filter(
            SalesOrder.status.in_(['draft', 'confirmed', 'processing'])
        ).count(),
        'open_tickets': ServiceTicket.query.filter(
            ServiceTicket.status.in_(['open', 'assigned', 'in_progress'])
        ).count(),
    }

    # Recent sales orders
    recent_orders = SalesOrder.query.order_by(
        SalesOrder.created_at.desc()
    ).limit(5).all()

    # Recent service tickets
    recent_tickets = ServiceTicket.query.order_by(
        ServiceTicket.ticket_date.desc()
    ).limit(5).all()

    # Low stock products
    low_stock_products = Product.query.join(Inventory).group_by(Product.id).having(
        func.sum(Inventory.quantity) <= Product.reorder_level
    ).limit(10).all()

    # Sales summary (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    sales_summary = db.session.query(
        func.sum(SalesOrder.total_amount).label('total_sales'),
        func.count(SalesOrder.id).label('order_count')
    ).filter(
        SalesOrder.order_date >= thirty_days_ago,
        SalesOrder.status != 'cancelled'
    ).first()

    return render_template(
        'index.html',
        stats=stats,
        recent_orders=recent_orders,
        recent_tickets=recent_tickets,
        low_stock_products=low_stock_products,
        sales_summary=sales_summary
    )


@dashboard_bp.route('/reports')
@login_required
def reports():
    """Reports page"""
    return render_template('reports.html')


@dashboard_bp.route('/analytics')
@login_required
def analytics():
    """Analytics page"""
    return render_template('analytics.html')

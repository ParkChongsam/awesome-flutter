"""
Helper functions
"""
from datetime import datetime
from decimal import Decimal


def format_currency(amount, currency='₩'):
    """Format amount as currency"""
    if amount is None:
        return f"{currency}0"

    if isinstance(amount, str):
        amount = Decimal(amount)

    return f"{currency}{amount:,.2f}"


def format_date(date_obj, format_str='%Y-%m-%d'):
    """Format date object"""
    if date_obj is None:
        return ''

    if isinstance(date_obj, str):
        return date_obj

    return date_obj.strftime(format_str)


def format_datetime(datetime_obj, format_str='%Y-%m-%d %H:%M:%S'):
    """Format datetime object"""
    if datetime_obj is None:
        return ''

    if isinstance(datetime_obj, str):
        return datetime_obj

    return datetime_obj.strftime(format_str)


def generate_code(prefix, model_class, field_name='code'):
    """Generate unique code for models"""
    today = datetime.utcnow()
    date_str = today.strftime('%Y%m%d')

    # Count existing codes for today
    search_pattern = f"{prefix}-{date_str}%"
    count = model_class.query.filter(
        getattr(model_class, field_name).like(search_pattern)
    ).count()

    return f"{prefix}-{date_str}-{count + 1:04d}"


def calculate_tax(amount, tax_rate=10.0):
    """Calculate tax amount"""
    if amount is None:
        return Decimal('0.00')

    amount = Decimal(str(amount))
    tax_rate = Decimal(str(tax_rate))

    return (amount * tax_rate / 100).quantize(Decimal('0.01'))


def calculate_discount(amount, discount_percent):
    """Calculate discount amount"""
    if amount is None or discount_percent is None:
        return Decimal('0.00')

    amount = Decimal(str(amount))
    discount_percent = Decimal(str(discount_percent))

    return (amount * discount_percent / 100).quantize(Decimal('0.01'))


def parse_decimal(value):
    """Safely parse value to Decimal"""
    if value is None or value == '':
        return Decimal('0.00')

    try:
        return Decimal(str(value)).quantize(Decimal('0.01'))
    except:
        return Decimal('0.00')


def parse_int(value, default=0):
    """Safely parse value to integer"""
    if value is None or value == '':
        return default

    try:
        return int(value)
    except:
        return default


def paginate_query(query, page=1, per_page=20):
    """Helper function for pagination"""
    return query.paginate(page=page, per_page=per_page, error_out=False)


def get_date_range(period='month'):
    """Get date range for reports"""
    today = datetime.utcnow()

    if period == 'today':
        start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = today

    elif period == 'week':
        start_date = today - timedelta(days=today.weekday())
        end_date = today

    elif period == 'month':
        start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = today

    elif period == 'quarter':
        quarter = (today.month - 1) // 3
        start_date = today.replace(month=quarter * 3 + 1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = today

    elif period == 'year':
        start_date = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = today

    else:
        start_date = today - timedelta(days=30)
        end_date = today

    return start_date, end_date

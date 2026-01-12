"""
WTForms for Flask ERP System
Place form classes here for data validation and input
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField, DecimalField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, NumberRange
from app.utils.validators import validate_korean_phone, validate_positive_number

# Example forms - expand as needed

class LoginForm(FlaskForm):
    """Login form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')


class RegistrationForm(FlaskForm):
    """User registration form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    full_name = StringField('Full Name', validators=[Length(max=120)])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters')
    ])
    password_confirm = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])


class CustomerForm(FlaskForm):
    """Customer creation/edit form"""
    customer_code = StringField('Customer Code', validators=[DataRequired(), Length(max=50)])
    company_name = StringField('Company Name', validators=[DataRequired(), Length(max=200)])
    phone = StringField('Phone', validators=[Optional(), validate_korean_phone])
    email = StringField('Email', validators=[Optional(), Email()])
    address = TextAreaField('Address', validators=[Optional(), Length(max=300)])
    city = StringField('City', validators=[Optional(), Length(max=100)])
    customer_type = SelectField('Customer Type', choices=[
        ('retail', 'Retail'),
        ('corporate', 'Corporate'),
        ('government', 'Government')
    ])
    credit_limit = DecimalField('Credit Limit', validators=[Optional(), validate_positive_number])
    notes = TextAreaField('Notes')


class ProductForm(FlaskForm):
    """Product creation/edit form"""
    product_code = StringField('Product Code', validators=[DataRequired(), Length(max=50)])
    name = StringField('Product Name', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description')
    category_id = SelectField('Category', coerce=int, validators=[Optional()])
    product_type = SelectField('Product Type', choices=[
        ('copy_machine', 'Copy Machine'),
        ('parts', 'Parts'),
        ('consumables', 'Consumables'),
        ('service', 'Service')
    ])
    manufacturer = StringField('Manufacturer', validators=[Optional(), Length(max=100)])
    model_number = StringField('Model Number', validators=[Optional(), Length(max=100)])
    cost_price = DecimalField('Cost Price', validators=[Optional(), validate_positive_number])
    selling_price = DecimalField('Selling Price', validators=[Optional(), validate_positive_number])
    retail_price = DecimalField('Retail Price', validators=[Optional(), validate_positive_number])
    reorder_level = IntegerField('Reorder Level', validators=[Optional(), NumberRange(min=0)])
    reorder_quantity = IntegerField('Reorder Quantity', validators=[Optional(), NumberRange(min=0)])


class SalesOrderForm(FlaskForm):
    """Sales order creation form"""
    customer_id = SelectField('Customer', coerce=int, validators=[DataRequired()])
    order_date = DateField('Order Date', validators=[DataRequired()])
    required_date = DateField('Required Date', validators=[Optional()])
    shipping_address = TextAreaField('Shipping Address')
    payment_terms = IntegerField('Payment Terms (days)', validators=[Optional(), NumberRange(min=0)])
    notes = TextAreaField('Notes')


class ServiceTicketForm(FlaskForm):
    """Service ticket creation form"""
    customer_id = SelectField('Customer', coerce=int, validators=[DataRequired()])
    product_id = SelectField('Equipment', coerce=int, validators=[Optional()])
    service_type = SelectField('Service Type', choices=[
        ('installation', 'Installation'),
        ('maintenance', 'Maintenance'),
        ('repair', 'Repair'),
        ('inspection', 'Inspection')
    ], validators=[DataRequired()])
    priority = SelectField('Priority', choices=[
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ], default='normal')
    problem_description = TextAreaField('Problem Description', validators=[DataRequired()])
    service_location = TextAreaField('Service Location')
    estimated_hours = DecimalField('Estimated Hours', validators=[Optional(), validate_positive_number])


# Add more forms as needed for other modules

# Flask ERP System - Project Structure Documentation

## Overview

This document provides a detailed overview of the Flask ERP system project structure for 참좋은복사기 (Very Good Copy Machine) company.

## Directory Structure

```
flask-erp-system/
│
├── app/                                    # Main application package
│   ├── __init__.py                        # Application factory and initialization
│   │
│   ├── models/                            # Database models (SQLAlchemy)
│   │   ├── __init__.py                   # Models export
│   │   ├── user.py                       # User and Role models
│   │   ├── customer.py                   # Customer and CustomerContact models
│   │   ├── supplier.py                   # Supplier and SupplierContact models
│   │   ├── product.py                    # Product and ProductCategory models
│   │   ├── inventory.py                  # Inventory, Warehouse, and Transaction models
│   │   ├── sales.py                      # SalesOrder, Invoice, and Payment models
│   │   ├── purchasing.py                 # PurchaseOrder and PurchaseOrderItem models
│   │   ├── service.py                    # ServiceTicket, Technician, and Schedule models
│   │   ├── accounting.py                 # Account, Transaction, and JournalEntry models
│   │   └── hr.py                         # Employee, Attendance, Payroll, and Department models
│   │
│   ├── blueprints/                       # Flask blueprints (modules)
│   │   ├── auth/                         # Authentication module
│   │   │   └── __init__.py              # Login, logout, registration routes
│   │   ├── dashboard/                    # Dashboard module
│   │   │   └── __init__.py              # Main dashboard and analytics
│   │   ├── inventory/                    # Inventory management module
│   │   │   └── __init__.py              # Products, stock, warehouses routes
│   │   ├── sales/                        # Sales management module
│   │   │   └── __init__.py              # Orders, invoices, payments routes
│   │   ├── purchasing/                   # Purchasing module
│   │   │   └── __init__.py              # Purchase orders, suppliers routes
│   │   ├── service/                      # Service management module
│   │   │   └── __init__.py              # Service tickets, technicians routes
│   │   ├── accounting/                   # Accounting module
│   │   │   └── __init__.py              # Accounts, journal entries routes
│   │   ├── hr/                          # Human Resources module
│   │   │   └── __init__.py              # Employees, payroll, attendance routes
│   │   └── crm/                         # Customer Relationship Management
│   │       └── __init__.py              # Customer management routes
│   │
│   ├── api/                             # REST API endpoints
│   │   └── __init__.py                  # API routes for integration
│   │
│   ├── forms/                           # WTForms for data validation
│   │   └── __init__.py                  # Form classes
│   │
│   ├── templates/                       # Jinja2 HTML templates
│   │   ├── base.html                    # Base template with navigation
│   │   ├── index.html                   # Landing page
│   │   ├── auth/                        # Authentication templates
│   │   │   ├── login.html
│   │   │   ├── register.html
│   │   │   ├── profile.html
│   │   │   └── change_password.html
│   │   ├── dashboard/                   # Dashboard templates
│   │   │   ├── index.html
│   │   │   ├── reports.html
│   │   │   └── analytics.html
│   │   ├── inventory/                   # Inventory templates
│   │   │   ├── index.html
│   │   │   ├── products.html
│   │   │   ├── product_detail.html
│   │   │   ├── add_product.html
│   │   │   ├── edit_product.html
│   │   │   ├── warehouses.html
│   │   │   ├── adjust_inventory.html
│   │   │   ├── transactions.html
│   │   │   └── categories.html
│   │   ├── sales/                       # Sales templates
│   │   │   ├── index.html
│   │   │   ├── new_order.html
│   │   │   ├── order_detail.html
│   │   │   ├── edit_order.html
│   │   │   ├── invoices.html
│   │   │   ├── invoice_detail.html
│   │   │   ├── payments.html
│   │   │   ├── customers.html
│   │   │   ├── customer_detail.html
│   │   │   └── sales_summary.html
│   │   ├── purchasing/                  # Purchasing templates
│   │   │   ├── index.html
│   │   │   ├── new_order.html
│   │   │   ├── order_detail.html
│   │   │   ├── receive_order.html
│   │   │   ├── suppliers.html
│   │   │   └── supplier_detail.html
│   │   ├── service/                     # Service templates
│   │   │   ├── index.html
│   │   │   ├── new_ticket.html
│   │   │   ├── ticket_detail.html
│   │   │   ├── technicians.html
│   │   │   └── schedule.html
│   │   ├── accounting/                  # Accounting templates
│   │   │   ├── index.html
│   │   │   ├── accounts.html
│   │   │   ├── journal_entries.html
│   │   │   ├── balance_sheet.html
│   │   │   └── income_statement.html
│   │   ├── hr/                         # HR templates
│   │   │   ├── index.html
│   │   │   ├── employees.html
│   │   │   ├── employee_detail.html
│   │   │   ├── attendance.html
│   │   │   ├── payroll.html
│   │   │   └── departments.html
│   │   ├── crm/                        # CRM templates
│   │   │   ├── index.html
│   │   │   ├── customers.html
│   │   │   ├── customer_detail.html
│   │   │   ├── new_customer.html
│   │   │   └── edit_customer.html
│   │   ├── shared/                     # Shared template components
│   │   │   ├── pagination.html
│   │   │   ├── table.html
│   │   │   └── form_macros.html
│   │   └── errors/                     # Error pages
│   │       ├── 404.html
│   │       ├── 403.html
│   │       └── 500.html
│   │
│   ├── static/                         # Static files (CSS, JS, images)
│   │   ├── css/
│   │   │   └── style.css              # Custom styles
│   │   ├── js/
│   │   │   └── main.js                # Custom JavaScript
│   │   └── img/
│   │       └── (image files)
│   │
│   └── utils/                          # Utility functions
│       ├── __init__.py
│       ├── helpers.py                  # Helper functions
│       ├── decorators.py               # Custom decorators
│       ├── validators.py               # Custom validators
│       └── seed.py                     # Database seeding
│
├── migrations/                         # Database migrations (Alembic)
│   └── versions/                       # Migration scripts
│
├── tests/                             # Unit and integration tests
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_routes.py
│   └── test_api.py
│
├── config.py                          # Application configuration
├── run.py                             # Application entry point
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variables template
├── .gitignore                         # Git ignore file
├── README.md                          # Project documentation
├── INSTALL.md                         # Installation guide
└── PROJECT_STRUCTURE.md               # This file
```

## Key Components

### 1. Application Factory (`app/__init__.py`)

The application factory pattern creates and configures the Flask application instance. It:
- Initializes Flask extensions (SQLAlchemy, Flask-Login, etc.)
- Registers blueprints
- Configures error handlers
- Sets up context processors

### 2. Models (`app/models/`)

SQLAlchemy ORM models representing database tables:
- **User Models**: Authentication and authorization
- **Business Models**: Customers, suppliers, products
- **Transaction Models**: Sales, purchases, inventory movements
- **Service Models**: Service tickets and technicians
- **Financial Models**: Accounting and payroll

### 3. Blueprints (`app/blueprints/`)

Modular components of the application:
- Each blueprint handles a specific business domain
- Contains route definitions and view functions
- Organized by module functionality

### 4. Templates (`app/templates/`)

Jinja2 HTML templates:
- **base.html**: Master template with navigation
- Module-specific templates for each feature
- Reusable components in `shared/`
- Error pages for common HTTP errors

### 5. Static Files (`app/static/`)

Frontend assets:
- **CSS**: Custom styles and theme
- **JavaScript**: Client-side functionality
- **Images**: Logos, icons, and media

### 6. API (`app/api/`)

RESTful API endpoints for:
- Product information
- Customer data
- Sales orders
- Inventory levels
- Integration with external systems

### 7. Forms (`app/forms/`)

WTForms classes for:
- Input validation
- CSRF protection
- Form rendering
- Data sanitization

### 8. Utilities (`app/utils/`)

Helper functions:
- **helpers.py**: Formatting, calculations
- **decorators.py**: Access control decorators
- **validators.py**: Custom validation rules
- **seed.py**: Database seeding scripts

### 9. Configuration (`config.py`)

Application settings:
- Development, testing, production configs
- Database connections
- Security settings
- Email configuration

### 10. Database Migrations (`migrations/`)

Alembic migration scripts:
- Version control for database schema
- Upgrade and downgrade scripts
- Migration history

## Module Descriptions

### Authentication Module
- User login and logout
- User registration
- Password management
- Session handling

### Dashboard Module
- Business metrics and KPIs
- Recent activity feeds
- Quick action shortcuts
- Analytics overview

### Inventory Module
- Product catalog management
- Stock level tracking
- Warehouse management
- Inventory adjustments
- Transaction history

### Sales Module
- Sales order processing
- Invoice generation
- Payment tracking
- Customer management
- Sales analytics

### Purchasing Module
- Purchase order creation
- Supplier management
- Goods receiving
- Purchase history

### Service Module
- Service ticket management
- Technician assignment
- Service scheduling
- Warranty tracking
- Customer feedback

### CRM Module
- Customer database
- Contact management
- Interaction history
- Opportunity tracking

### Accounting Module
- Chart of accounts
- Journal entries
- Financial reports
- Transaction recording

### HR Module
- Employee records
- Attendance tracking
- Payroll processing
- Department management

## Design Patterns

### 1. Application Factory Pattern
Creates configured Flask application instances.

### 2. Blueprint Pattern
Modular application structure with separate components.

### 3. MVC Pattern
- **Models**: Data layer (SQLAlchemy models)
- **Views**: Presentation layer (Jinja2 templates)
- **Controllers**: Business logic (Blueprint routes)

### 4. Repository Pattern
Database access abstraction through SQLAlchemy ORM.

### 5. Decorator Pattern
Access control and route protection using custom decorators.

## Best Practices

1. **Separation of Concerns**: Each module handles specific functionality
2. **DRY Principle**: Reusable components and utilities
3. **Security First**: CSRF protection, password hashing, input validation
4. **Scalability**: Modular design allows easy expansion
5. **Maintainability**: Clear structure and documentation
6. **Testing**: Organized test suite structure

## Adding New Features

To add a new module:

1. Create model in `app/models/`
2. Create blueprint in `app/blueprints/`
3. Create templates in `app/templates/`
4. Add forms in `app/forms/`
5. Register blueprint in `app/__init__.py`
6. Create migration: `flask db migrate`
7. Run migration: `flask db upgrade`

## Naming Conventions

- **Files**: lowercase with underscores (snake_case)
- **Classes**: PascalCase
- **Functions**: lowercase with underscores (snake_case)
- **Constants**: UPPERCASE with underscores
- **Templates**: lowercase with underscores
- **URLs**: lowercase with hyphens

---

**참좋은복사기 (Very Good Copy Machine) - ERP System**

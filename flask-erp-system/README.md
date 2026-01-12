# Flask ERP System - 참좋은복사기 (Very Good Copy Machine)

A comprehensive Enterprise Resource Planning (ERP) system built with Flask for managing copy machine sales, service, and maintenance operations.

## Features

### Core Modules

1. **Dashboard**
   - Real-time business metrics and KPIs
   - Recent orders and service tickets
   - Quick action shortcuts
   - Analytics overview

2. **Inventory Management**
   - Product catalog management
   - Multi-warehouse inventory tracking
   - Stock level monitoring and alerts
   - Inventory transactions history
   - Product categories and classifications

3. **Sales Management**
   - Sales order processing
   - Customer management
   - Invoice generation
   - Payment tracking
   - Sales reports and analytics

4. **Purchasing Management**
   - Purchase order creation
   - Supplier management
   - Goods receiving
   - Purchase history tracking

5. **Service Management**
   - Service ticket creation and tracking
   - Technician assignment and scheduling
   - Service history and maintenance records
   - Customer feedback collection
   - Warranty management

6. **Customer Relationship Management (CRM)**
   - Customer database
   - Contact management
   - Customer interaction history
   - Sales opportunity tracking

7. **Accounting**
   - Chart of accounts
   - Journal entries
   - Financial reports (Balance Sheet, Income Statement)
   - Transaction tracking

8. **Human Resources**
   - Employee management
   - Attendance tracking
   - Payroll processing
   - Department management

9. **REST API**
   - RESTful API endpoints for integration
   - JSON-based data exchange
   - Authentication and authorization

## Technology Stack

- **Backend Framework**: Flask 3.0
- **Database**: SQLAlchemy (SQLite/PostgreSQL/MySQL)
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF, WTForms
- **Frontend**: Bootstrap 5, jQuery, Font Awesome
- **API**: Flask-RESTful
- **Migration**: Flask-Migrate (Alembic)
- **Email**: Flask-Mail

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Instructions

1. **Clone or extract the project**
   ```bash
   cd flask-erp-system
   ```

2. **Create and activate virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy example environment file
   cp .env.example .env

   # Edit .env file with your settings
   nano .env
   ```

5. **Initialize the database**
   ```bash
   # Create database tables and seed initial data
   flask init-db
   ```

6. **Create admin user (alternative method)**
   ```bash
   flask create-admin
   ```

7. **Run the application**
   ```bash
   # Development mode
   python run.py

   # Or using Flask CLI
   flask run
   ```

8. **Access the application**
   - Open browser and navigate to: `http://localhost:5000`
   - Default admin credentials:
     - Username: `admin`
     - Password: `admin123`

## Project Structure

```
flask-erp-system/
├── app/
│   ├── __init__.py              # Application factory
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   ├── user.py             # User and authentication
│   │   ├── customer.py         # Customer models
│   │   ├── supplier.py         # Supplier models
│   │   ├── product.py          # Product models
│   │   ├── inventory.py        # Inventory models
│   │   ├── sales.py            # Sales models
│   │   ├── purchasing.py       # Purchase order models
│   │   ├── service.py          # Service ticket models
│   │   ├── accounting.py       # Accounting models
│   │   └── hr.py               # HR models
│   ├── blueprints/             # Application blueprints
│   │   ├── auth/               # Authentication
│   │   ├── dashboard/          # Dashboard
│   │   ├── inventory/          # Inventory management
│   │   ├── sales/              # Sales management
│   │   ├── purchasing/         # Purchasing management
│   │   ├── service/            # Service management
│   │   ├── accounting/         # Accounting
│   │   ├── hr/                 # Human resources
│   │   └── crm/                # Customer relationship
│   ├── api/                    # REST API endpoints
│   ├── forms/                  # WTForms classes
│   ├── templates/              # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── inventory/
│   │   ├── sales/
│   │   ├── purchasing/
│   │   ├── service/
│   │   ├── accounting/
│   │   ├── hr/
│   │   ├── crm/
│   │   ├── shared/
│   │   └── errors/
│   ├── static/                 # Static files
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── main.js
│   │   └── img/
│   └── utils/                  # Utility functions
│       ├── helpers.py
│       ├── decorators.py
│       ├── validators.py
│       └── seed.py
├── migrations/                 # Database migrations
├── tests/                      # Unit tests
├── config.py                   # Configuration
├── run.py                      # Application entry point
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables example
├── .gitignore                 # Git ignore file
└── README.md                  # This file
```

## Configuration

Edit the `.env` file to configure:

- **Database**: SQLite (default), PostgreSQL, or MySQL
- **Secret Key**: For session encryption
- **Mail Server**: For sending emails
- **Company Information**: Name and details

### Database Configuration

**SQLite (Default - Development)**
```
DATABASE_URL=sqlite:///erp.db
```

**PostgreSQL (Production)**
```
DATABASE_URL=postgresql://username:password@localhost/erp_db
```

**MySQL**
```
DATABASE_URL=mysql+pymysql://username:password@localhost/erp_db
```

## Usage

### Default Admin Account

- **Username**: admin
- **Password**: admin123

⚠️ **Important**: Change the default password after first login!

### Creating Users

1. Login as admin
2. Navigate to User Management
3. Create new users with appropriate roles

### Available Roles

- **admin**: Full system access
- **manager**: Management access
- **sales**: Sales module access
- **warehouse**: Inventory module access
- **accountant**: Accounting module access
- **technician**: Service module access

## API Documentation

The system provides RESTful API endpoints for integration:

### Base URL
```
http://localhost:5000/api
```

### Endpoints

**Products**
- `GET /api/products` - List all products
- `GET /api/products/<id>` - Get product details

**Customers**
- `GET /api/customers` - List all customers
- `GET /api/customers/<id>` - Get customer details

**Sales Orders**
- `GET /api/sales-orders` - List sales orders

**Inventory**
- `GET /api/inventory` - Get inventory levels

**Health Check**
- `GET /api/health` - API health status

### Authentication

All API endpoints (except health check) require authentication using Flask-Login session cookies.

## Database Schema

The system uses SQLAlchemy ORM with the following main entities:

- **Users & Roles**: User authentication and authorization
- **Customers**: Customer information and contacts
- **Suppliers**: Supplier/vendor information
- **Products**: Product catalog and specifications
- **Inventory**: Stock levels and warehouses
- **Sales Orders**: Customer orders and invoices
- **Purchase Orders**: Supplier orders
- **Service Tickets**: Service requests and maintenance
- **Accounts**: Chart of accounts for accounting
- **Employees**: HR and employee records

## Development

### Running Tests

```bash
pytest
```

### Database Migrations

```bash
# Create a migration
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback migration
flask db downgrade
```

### Code Style

The project follows PEP 8 style guidelines. Format code using:

```bash
black .
flake8 .
```

## Deployment

### Production Considerations

1. **Change Secret Key**: Use a strong, random secret key
2. **Use Production Database**: PostgreSQL or MySQL
3. **Enable HTTPS**: Use SSL/TLS certificates
4. **Set Debug to False**: In production configuration
5. **Configure Mail Server**: For email notifications
6. **Set up Backups**: Regular database backups
7. **Use WSGI Server**: Gunicorn or uWSGI

### Example with Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

### Docker Deployment

```bash
# Build image
docker build -t flask-erp .

# Run container
docker run -d -p 5000:5000 --name erp-system flask-erp
```

## Features in Detail

### Inventory Management
- Multi-warehouse support
- Real-time stock tracking
- Low stock alerts
- Inventory adjustments
- Transaction history
- Product categories

### Sales Management
- Order creation and tracking
- Invoice generation
- Payment recording
- Customer credit limits
- Sales analytics
- Order status workflow

### Service Management
- Service ticket creation
- Technician scheduling
- Service history tracking
- Parts tracking
- Warranty management
- Customer satisfaction ratings

### Accounting
- Double-entry bookkeeping
- Chart of accounts
- Journal entries
- Financial reports
- Trial balance
- Tax calculation

## Security Features

- Password hashing (Werkzeug)
- Session management
- CSRF protection
- SQL injection prevention (SQLAlchemy ORM)
- Role-based access control
- Failed login attempt tracking

## Support

For issues, questions, or contributions:

1. Check existing documentation
2. Review code comments
3. Create an issue in the repository

## License

This project is proprietary software for 참좋은복사기 (Very Good Copy Machine) Company.

## Credits

Developed for **참좋은복사기 (Very Good Copy Machine)** - A leading copy machine sales and service company in South Korea.

## Version History

- **1.0.0** (2024) - Initial release
  - Core ERP modules
  - Multi-module support
  - REST API
  - Responsive design

---

**참좋은복사기 (Very Good Copy Machine) - ERP System**
© 2024 All Rights Reserved

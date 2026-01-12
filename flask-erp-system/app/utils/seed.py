"""
Database seeding utility
"""
from app import db
from app.models import (
    Role, User, Customer, Supplier, Product, ProductCategory,
    Warehouse, Inventory, Department
)
from werkzeug.security import generate_password_hash
from datetime import datetime


def seed_database():
    """Seed database with initial data"""

    # Create roles
    print("Creating roles...")
    roles = [
        Role(name='admin', description='시스템 관리자 (System Administrator)'),
        Role(name='manager', description='매니저 (Manager)'),
        Role(name='sales', description='영업 담당자 (Sales Representative)'),
        Role(name='warehouse', description='창고 담당자 (Warehouse Staff)'),
        Role(name='accountant', description='회계 담당자 (Accountant)'),
        Role(name='technician', description='기술자 (Technician)'),
    ]

    for role in roles:
        existing = Role.query.filter_by(name=role.name).first()
        if not existing:
            db.session.add(role)

    db.session.commit()

    # Create admin user
    print("Creating admin user...")
    admin_role = Role.query.filter_by(name='admin').first()
    admin_user = User.query.filter_by(username='admin').first()

    if not admin_user:
        admin_user = User(
            username='admin',
            email='admin@chamjoheum.com',
            full_name='시스템 관리자',
            role=admin_role,
            is_active=True
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created: username='admin', password='admin123'")

    # Create product categories
    print("Creating product categories...")
    categories = [
        ProductCategory(name='복사기 (Copy Machines)', code='CAT-001', description='복사기 및 프린터'),
        ProductCategory(name='부품 (Parts)', code='CAT-002', description='복사기 부품'),
        ProductCategory(name='소모품 (Consumables)', code='CAT-003', description='토너, 잉크 등'),
        ProductCategory(name='서비스 (Services)', code='CAT-004', description='유지보수 서비스'),
    ]

    for cat in categories:
        existing = ProductCategory.query.filter_by(code=cat.code).first()
        if not existing:
            db.session.add(cat)

    db.session.commit()

    # Create warehouses
    print("Creating warehouses...")
    warehouses = [
        Warehouse(code='WH-001', name='본사 창고 (Main Warehouse)', city='서울', is_active=True),
        Warehouse(code='WH-002', name='지사 창고 (Branch Warehouse)', city='부산', is_active=True),
    ]

    for wh in warehouses:
        existing = Warehouse.query.filter_by(code=wh.code).first()
        if not existing:
            db.session.add(wh)

    db.session.commit()

    # Create departments
    print("Creating departments...")
    departments = [
        Department(code='DEPT-001', name='영업부 (Sales)', description='Sales Department'),
        Department(code='DEPT-002', name='기술지원부 (Technical Support)', description='Technical Support'),
        Department(code='DEPT-003', name='관리부 (Administration)', description='Administration'),
        Department(code='DEPT-004', name='물류부 (Logistics)', description='Logistics'),
    ]

    for dept in departments:
        existing = Department.query.filter_by(code=dept.code).first()
        if not existing:
            db.session.add(dept)

    db.session.commit()

    # Create sample products
    print("Creating sample products...")
    copy_machine_cat = ProductCategory.query.filter_by(code='CAT-001').first()
    consumables_cat = ProductCategory.query.filter_by(code='CAT-003').first()

    products = [
        Product(
            product_code='PROD-001',
            name='삼성 복합기 X3280NR',
            description='A3 컬러 레이저 복합기',
            category=copy_machine_cat,
            product_type='copy_machine',
            manufacturer='Samsung',
            model_number='X3280NR',
            cost_price=1500000,
            selling_price=1800000,
            retail_price=2000000,
            print_speed=32,
            color_support=True,
            duplex_support=True,
            network_support=True,
            is_active=True
        ),
        Product(
            product_code='PROD-002',
            name='HP LaserJet Pro MFP M428fdw',
            description='A4 흑백 레이저 복합기',
            category=copy_machine_cat,
            product_type='copy_machine',
            manufacturer='HP',
            model_number='M428fdw',
            cost_price=500000,
            selling_price=600000,
            retail_price=650000,
            print_speed=38,
            color_support=False,
            duplex_support=True,
            network_support=True,
            is_active=True
        ),
        Product(
            product_code='PROD-003',
            name='토너 카트리지 - 검정',
            description='범용 검정 토너',
            category=consumables_cat,
            product_type='consumables',
            cost_price=30000,
            selling_price=45000,
            retail_price=50000,
            is_active=True
        ),
    ]

    for prod in products:
        existing = Product.query.filter_by(product_code=prod.product_code).first()
        if not existing:
            db.session.add(prod)

    db.session.commit()

    # Create sample customers
    print("Creating sample customers...")
    customers = [
        Customer(
            customer_code='CUST-001',
            company_name='㈜대한무역',
            phone='02-1234-5678',
            email='contact@daehan.com',
            address='서울시 강남구 테헤란로 123',
            city='서울',
            customer_type='corporate',
            status='active'
        ),
        Customer(
            customer_code='CUST-002',
            company_name='한국산업㈜',
            phone='02-2345-6789',
            email='info@hanguk.com',
            address='서울시 송파구 올림픽로 456',
            city='서울',
            customer_type='corporate',
            status='active'
        ),
    ]

    for cust in customers:
        existing = Customer.query.filter_by(customer_code=cust.customer_code).first()
        if not existing:
            db.session.add(cust)

    db.session.commit()

    # Create sample suppliers
    print("Creating sample suppliers...")
    suppliers = [
        Supplier(
            supplier_code='SUP-001',
            company_name='삼성전자 판매㈜',
            phone='02-3456-7890',
            email='sales@samsung.com',
            address='서울시 서초구 서초대로 74길 11',
            city='서울',
            supplier_type='manufacturer',
            status='active'
        ),
        Supplier(
            supplier_code='SUP-002',
            company_name='HP Korea',
            phone='02-4567-8901',
            email='sales@hp.com',
            address='서울시 강남구 테헤란로 152',
            city='서울',
            supplier_type='manufacturer',
            status='active'
        ),
    ]

    for sup in suppliers:
        existing = Supplier.query.filter_by(supplier_code=sup.supplier_code).first()
        if not existing:
            db.session.add(sup)

    db.session.commit()

    print("Database seeding completed successfully!")

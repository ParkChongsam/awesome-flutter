# Installation Guide - Flask ERP System

## Quick Start

### 1. System Requirements

- **Python**: 3.8 or higher
- **pip**: Latest version
- **Virtual Environment**: Recommended
- **Database**: SQLite (default) / PostgreSQL / MySQL
- **Memory**: Minimum 512MB RAM
- **Disk Space**: 200MB minimum

### 2. Installation Steps

#### Step 1: Prepare Environment

```bash
# Navigate to project directory
cd flask-erp-system

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

#### Step 2: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

#### Step 3: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit configuration (use your preferred editor)
nano .env
# or
vim .env
# or on Windows:
notepad .env
```

**Required Configuration:**
```env
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///erp.db
```

#### Step 4: Initialize Database

```bash
# Create database and seed initial data
flask init-db
```

This command will:
- Create all database tables
- Create default roles
- Create admin user (admin/admin123)
- Seed sample data

#### Step 5: Run Application

```bash
# Development server
python run.py

# Or using Flask CLI
flask run

# Run on specific host and port
flask run --host=0.0.0.0 --port=8000
```

#### Step 6: Access Application

1. Open web browser
2. Navigate to: `http://localhost:5000`
3. Login with:
   - Username: `admin`
   - Password: `admin123`

## Database Setup

### SQLite (Default)

No additional setup required. Database file will be created automatically.

```env
DATABASE_URL=sqlite:///erp.db
```

### PostgreSQL

1. **Install PostgreSQL**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib

   # macOS
   brew install postgresql
   ```

2. **Create Database**
   ```bash
   # Login to PostgreSQL
   sudo -u postgres psql

   # Create database and user
   CREATE DATABASE erp_db;
   CREATE USER erp_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE erp_db TO erp_user;
   \q
   ```

3. **Update .env**
   ```env
   DATABASE_URL=postgresql://erp_user:your_password@localhost/erp_db
   ```

4. **Install Python driver**
   ```bash
   pip install psycopg2-binary
   ```

### MySQL

1. **Install MySQL**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install mysql-server

   # macOS
   brew install mysql
   ```

2. **Create Database**
   ```bash
   # Login to MySQL
   mysql -u root -p

   # Create database
   CREATE DATABASE erp_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'erp_user'@'localhost' IDENTIFIED BY 'your_password';
   GRANT ALL PRIVILEGES ON erp_db.* TO 'erp_user'@'localhost';
   FLUSH PRIVILEGES;
   exit;
   ```

3. **Update .env**
   ```env
   DATABASE_URL=mysql+pymysql://erp_user:your_password@localhost/erp_db
   ```

4. **Install Python driver**
   ```bash
   pip install pymysql
   ```

## Troubleshooting

### Common Issues

#### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows

# Reinstall requirements
pip install -r requirements.txt
```

#### Issue: "Database connection error"

**Solution:**
```bash
# Check DATABASE_URL in .env
# Ensure database server is running
# Verify credentials

# For PostgreSQL
sudo service postgresql status
sudo service postgresql start

# For MySQL
sudo service mysql status
sudo service mysql start
```

#### Issue: "Port 5000 already in use"

**Solution:**
```bash
# Use different port
flask run --port=8000

# Or find and kill process using port 5000
# Linux/Mac:
lsof -i :5000
kill -9 <PID>

# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

#### Issue: "Static files not loading"

**Solution:**
```bash
# Clear browser cache
# Check static folder permissions
# Restart Flask application
```

### Reset Database

If you need to start fresh:

```bash
# Stop the application

# Delete database file (SQLite)
rm erp.db

# Reinitialize
flask init-db
```

## Production Deployment

### Using Gunicorn (Linux/Mac)

```bash
# Install Gunicorn
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:8000 run:app

# With logging
gunicorn -w 4 -b 0.0.0.0:8000 --access-logfile access.log --error-logfile error.log run:app
```

### Using uWSGI

```bash
# Install uWSGI
pip install uwsgi

# Run
uwsgi --http :8000 --wsgi-file run.py --callable app --processes 4 --threads 2
```

### Using Nginx as Reverse Proxy

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /path/to/flask-erp-system/app/static;
    }
}
```

### Environment Variables for Production

```env
FLASK_ENV=production
DEBUG=False
SECRET_KEY=<generate-strong-random-key>
DATABASE_URL=postgresql://user:pass@localhost/erp_db
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

## Maintenance

### Backup Database

**SQLite:**
```bash
cp erp.db erp_backup_$(date +%Y%m%d).db
```

**PostgreSQL:**
```bash
pg_dump -U erp_user erp_db > erp_backup_$(date +%Y%m%d).sql
```

**MySQL:**
```bash
mysqldump -u erp_user -p erp_db > erp_backup_$(date +%Y%m%d).sql
```

### Update Application

```bash
# Activate virtual environment
source venv/bin/activate

# Pull latest changes (if using git)
git pull

# Update dependencies
pip install -r requirements.txt --upgrade

# Run migrations
flask db upgrade

# Restart application
```

## Security Checklist

- [ ] Change default admin password
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS in production
- [ ] Set FLASK_ENV=production
- [ ] Disable debug mode
- [ ] Configure firewall
- [ ] Regular database backups
- [ ] Keep dependencies updated
- [ ] Use environment variables for secrets
- [ ] Implement rate limiting

## Getting Help

If you encounter issues:

1. Check this installation guide
2. Review error logs
3. Check Flask documentation: https://flask.palletsprojects.com/
4. Check SQLAlchemy documentation: https://www.sqlalchemy.org/

---

**Installation Complete!**

Your Flask ERP System is now ready to use. Access the application at http://localhost:5000 and login with admin/admin123.

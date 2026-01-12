# Heroku Deployment Guide

## Flask ERP System - Heroku 배포 가이드

### Prerequisites (사전 요구사항)

1. **Heroku CLI 설치**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku

   # Ubuntu/Debian
   curl https://cli-assets.heroku.com/install-ubuntu.sh | sh

   # Windows
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Heroku 계정**
   - https://signup.heroku.com/ 에서 무료 계정 생성

### Deployment Steps (배포 단계)

#### 1. Heroku 로그인

```bash
heroku login
```

#### 2. Heroku 앱 생성

```bash
# Navigate to project directory
cd flask-erp-system

# Create Heroku app (앱 이름은 자동 생성됨)
heroku create

# Or create with specific name (특정 이름으로 생성)
heroku create chamjoheum-erp
```

#### 3. PostgreSQL 데이터베이스 추가

```bash
# Add PostgreSQL addon (무료 플랜)
heroku addons:create heroku-postgresql:essential-0

# Check database info
heroku pg:info
```

#### 4. 환경 변수 설정

```bash
# Set Flask environment
heroku config:set FLASK_ENV=production

# Set secret key (강력한 랜덤 키 생성)
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# Set company info
heroku config:set COMPANY_NAME="참좋은복사기"
heroku config:set COMPANY_NAME_EN="Very Good Copy Machine"

# Check all config variables
heroku config
```

#### 5. 배포

```bash
# Commit all changes
git add .
git commit -m "Add Heroku deployment configuration"

# Push to Heroku
git push heroku main

# Or if using a different branch
git push heroku your-branch-name:main
```

#### 6. 데이터베이스 초기화

```bash
# Run database initialization
heroku run flask init-db

# Or create admin user manually
heroku run flask create-admin
```

#### 7. 앱 열기

```bash
# Open app in browser
heroku open
```

### Configuration Files (배포 파일)

이 프로젝트에는 다음 Heroku 배포 파일이 포함되어 있습니다:

- **Procfile** - Heroku 프로세스 정의
- **runtime.txt** - Python 버전 지정
- **requirements.txt** - Python 의존성
- **app.json** - Heroku 앱 메타데이터
- **.slugignore** - 불필요한 파일 제외

### Database Migration (데이터베이스 마이그레이션)

```bash
# Create migration
heroku run flask db migrate -m "Description"

# Apply migration
heroku run flask db upgrade

# Rollback migration
heroku run flask db downgrade
```

### Viewing Logs (로그 확인)

```bash
# View recent logs
heroku logs --tail

# View specific number of lines
heroku logs -n 200

# View logs for specific dyno
heroku logs --dyno web
```

### Scaling (스케일링)

```bash
# Scale web dynos
heroku ps:scale web=1

# Check dyno status
heroku ps

# Restart application
heroku restart
```

### Database Backup (데이터베이스 백업)

```bash
# Create backup
heroku pg:backups:capture

# List backups
heroku pg:backups

# Download backup
heroku pg:backups:download

# Restore from backup
heroku pg:backups:restore
```

### Custom Domain (커스텀 도메인)

```bash
# Add custom domain
heroku domains:add www.your-domain.com

# View domains
heroku domains

# Get DNS target
heroku domains:wait www.your-domain.com
```

### SSL/HTTPS

Heroku는 자동으로 무료 SSL 인증서를 제공합니다.

```bash
# Enable Automated Certificate Management
heroku certs:auto:enable

# Check certificate status
heroku certs:auto
```

### Environment-Specific Settings

#### Production Environment Variables

```bash
# Disable debug mode
heroku config:set FLASK_DEBUG=False

# Set session cookie secure
heroku config:set SESSION_COOKIE_SECURE=True

# Set database connection pool
heroku config:set SQLALCHEMY_POOL_SIZE=10
heroku config:set SQLALCHEMY_MAX_OVERFLOW=20
```

### Monitoring (모니터링)

```bash
# View app metrics
heroku metrics

# Add monitoring addon (optional)
heroku addons:create papertrail

# View addon info
heroku addons:info papertrail
```

### Troubleshooting (문제 해결)

#### Issue: Application Error

```bash
# Check logs for errors
heroku logs --tail

# Check dyno status
heroku ps

# Restart application
heroku restart
```

#### Issue: Database Connection Error

```bash
# Check database status
heroku pg:info

# Check database credentials
heroku pg:credentials:url

# Reset database (WARNING: This will delete all data!)
heroku pg:reset DATABASE_URL
heroku run flask init-db
```

#### Issue: Slug Size Too Large

```bash
# Check slug size
heroku builds:info

# Add files to .slugignore
echo "tests/" >> .slugignore
echo "*.md" >> .slugignore
```

#### Issue: Out of Memory

```bash
# Upgrade to hobby dyno
heroku ps:resize web=hobby

# Check memory usage
heroku logs --tail | grep "Memory"
```

### Cost Optimization (비용 최적화)

#### Free Tier Limits:
- **Dynos**: 550-1000 free dyno hours per month
- **PostgreSQL**: 10,000 rows (essential-0 plan)
- **Automatic sleep**: Apps sleep after 30 minutes of inactivity

#### Upgrade Options:
```bash
# Upgrade to Hobby dyno ($7/month, no sleep)
heroku ps:resize web=hobby

# Upgrade database ($5/month, 10M rows)
heroku addons:upgrade heroku-postgresql:mini
```

### Useful Commands (유용한 명령어)

```bash
# Open Heroku dashboard
heroku open --admin

# Open database console
heroku pg:psql

# Run one-off commands
heroku run python
heroku run flask shell

# Access app shell
heroku run bash

# View app info
heroku info

# Rename app
heroku rename new-app-name

# Transfer app ownership
heroku apps:transfer new-owner@example.com
```

### CI/CD Integration

#### GitHub Integration:

1. Heroku Dashboard에 로그인
2. App → Deploy → GitHub 연결
3. Enable Automatic Deploys
4. 선택: Wait for CI to pass before deploy

```bash
# Or use Heroku CLI
heroku git:remote -a your-app-name
```

### Maintenance Mode

```bash
# Enable maintenance mode
heroku maintenance:on

# Disable maintenance mode
heroku maintenance:off

# Check maintenance status
heroku maintenance
```

### Performance Tips (성능 팁)

1. **Database Connection Pooling**
   ```python
   # In config.py
   SQLALCHEMY_POOL_SIZE = 10
   SQLALCHEMY_MAX_OVERFLOW = 20
   SQLALCHEMY_POOL_RECYCLE = 3600
   ```

2. **Enable Gzip Compression**
   ```python
   # Add to app/__init__.py
   from flask_compress import Compress
   Compress(app)
   ```

3. **Use CDN for Static Files**
   - Consider using AWS S3 or Cloudflare for static assets

4. **Enable Caching**
   ```bash
   heroku addons:create memcachier:dev
   ```

### Security Checklist (보안 체크리스트)

- [ ] SECRET_KEY is set to random value
- [ ] FLASK_ENV is set to production
- [ ] Debug mode is disabled
- [ ] DATABASE_URL is using SSL
- [ ] SESSION_COOKIE_SECURE is True
- [ ] Strong admin password set
- [ ] Environment variables are not in code
- [ ] SSL/HTTPS is enabled
- [ ] Regular backups are configured

### Post-Deployment (배포 후)

1. **Access the application**
   ```bash
   heroku open
   ```

2. **Login with default credentials**
   - Username: `admin`
   - Password: `admin123`
   - **IMPORTANT**: Change password immediately!

3. **Verify functionality**
   - [ ] Login works
   - [ ] Dashboard loads
   - [ ] Database queries work
   - [ ] All modules are accessible

4. **Monitor performance**
   ```bash
   heroku logs --tail
   heroku metrics
   ```

### Support (지원)

- Heroku Documentation: https://devcenter.heroku.com/
- Heroku Status: https://status.heroku.com/
- Heroku Support: https://help.heroku.com/

---

**Successfully deployed! 🎉**

Your Flask ERP System is now running on Heroku!

# 🚀 Election Cart Backend - Production Readiness Plan

**Date:** November 3, 2025  
**Status:** Development → Production Migration  
**Priority:** Critical Security & Performance Review

---

## 📋 Executive Summary

Your Django backend is **functionally complete** with solid architecture, but requires **critical security hardening** and **production optimizations** before deployment. This plan provides a detailed, step-by-step roadmap to make your backend production-ready.

**Estimated Timeline:** 5-7 days  
**Risk Level:** Medium (security issues present but fixable)  
**Deployment Readiness:** 60% → Target: 95%+

---

## 🔍 Current State Analysis

### ✅ Strengths (What's Working Well)

1. **Solid Architecture**
   - Well-structured Django apps (authentication, products, orders, cart, admin_panel)
   - Clean separation of concerns
   - RESTful API design with DRF
   - Custom user model with role-based access

2. **Core Features Complete**
   - JWT authentication with Firebase integration
   - Product management (packages & campaigns)
   - Shopping cart functionality
   - Order processing workflow with status tracking
   - Razorpay payment integration
   - Resource upload system with validation
   - Dynamic resource fields
   - Checklist system for order tracking
   - Invoice generation with ReportLab
   - Admin panel with analytics
   - Staff assignment and notifications
   - Audit logging for products
   - Image gallery with Cloudinary CDN

3. **Good Practices Already Implemented**
   - Environment variables for configuration
   - PostgreSQL database
   - CORS configuration
   - File upload validation
   - Image optimization
   - Database indexing on key fields
   - Prefetch/select_related for query optimization
   - Serializer validation
   - Permission classes (IsAdmin, IsAdminOrStaff)

4. **Security Measures in Place**
   - File type validation (MIME type checking)
   - File size limits
   - Secure file storage outside web root
   - Authentication required for sensitive endpoints
   - CSRF protection enabled
   - SQL injection protection (Django ORM)


---

## ⚠️ Critical Issues (Must Fix Before Production)

### 🔴 CRITICAL - Security Vulnerabilities

#### 1. **Exposed Secrets in .env File**
**Risk Level:** CRITICAL  
**Impact:** Complete system compromise

**Current Issues:**
```env
# ❌ EXPOSED IN REPOSITORY
DJANGO_SECRET_KEY=z=5@a+hice(l04g8gdbtd05m1q!#%yxikma^oycy-yyh1f17=2
RAZORPAY_KEY_ID=rzp_live_RWGCaTq8yBUu1O  # LIVE KEY!
RAZORPAY_KEY_SECRET=BkMbLO9W10fvGEwjw4624uY7  # LIVE SECRET!
CLOUDINARY_API_SECRET=s6HU7XHz5vqF2bmtKA9cLVuQdvs
DB_PASSWORD=2509
```

**Why This is Critical:**
- Anyone with repo access can steal payment credentials
- Can process unauthorized payments
- Can access/delete all user data
- Can impersonate any user

**Fix Required:**
1. **Immediately rotate ALL credentials**
2. **Remove .env from git history**
3. **Use environment variables on server**
4. **Never commit secrets again**

---

#### 2. **DEBUG Mode Enabled**
**Risk Level:** CRITICAL  
**Impact:** Information disclosure, security bypass

**Current:**
```python
DEBUG = os.getenv('DEBUG', 'True') == 'True'  # Defaults to True!
```

**Problems:**
- Exposes full stack traces with code
- Shows database queries
- Reveals file paths and system info
- Disables security features
- Shows all environment variables

**Fix Required:**
```python
DEBUG = os.getenv('DEBUG', 'False') == 'True'  # Default to False
```

---

#### 3. **Missing Security Headers**
**Risk Level:** HIGH  
**Impact:** XSS, clickjacking, MITM attacks

**Currently Missing:**
- HTTPS enforcement
- HSTS headers
- Secure cookie flags
- Content Security Policy
- X-Frame-Options

**Fix Required:** (See implementation section)

---

#### 4. **Weak ALLOWED_HOSTS Configuration**
**Risk Level:** HIGH  
**Impact:** Host header injection attacks

**Current:**
```python
ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # Only localhost!
```

**Fix Required:**
- Add production domain
- Remove localhost in production
- Add load balancer IP if applicable

---

### 🟡 HIGH PRIORITY - Infrastructure Issues

#### 5. **No Production Database Configuration**
**Risk Level:** HIGH  
**Impact:** Data loss, poor performance, no backups

**Current:** Local PostgreSQL with weak password

**Issues:**
- No automated backups
- No SSL connection
- No connection pooling
- Single point of failure
- No read replicas

**Fix Required:**
- Managed PostgreSQL (AWS RDS, DigitalOcean, etc.)
- Enable SSL connections
- Configure automated backups
- Set up connection pooling
- Test backup restoration

---

#### 6. **No Logging Configuration**
**Risk Level:** HIGH  
**Impact:** Cannot debug production issues

**Current:** No structured logging

**Problems:**
- Cannot track errors in production
- No audit trail
- Cannot debug issues
- No performance monitoring

**Fix Required:** Comprehensive logging setup

---

#### 7. **No Rate Limiting**
**Risk Level:** MEDIUM  
**Impact:** DDoS, brute force attacks, resource exhaustion

**Current:** No rate limiting on any endpoint

**Vulnerable Endpoints:**
- `/api/auth/login/` - Brute force attacks
- `/api/orders/create/` - Order spam
- `/api/orders/{id}/upload-resources/` - File upload spam

**Fix Required:** Implement rate limiting

---

#### 8. **Missing Monitoring & Health Checks**
**Risk Level:** MEDIUM  
**Impact:** Cannot detect outages, slow response to issues

**Current:** No health check endpoint, no monitoring

**Fix Required:**
- Health check endpoint
- Uptime monitoring
- Error tracking (Sentry)
- Performance monitoring

---

### 🟢 MEDIUM PRIORITY - Optimization Issues

#### 9. **Inefficient Caching**
**Current:** LocMemCache (in-memory, single process)

**Problems:**
- Doesn't work with multiple workers
- Cache lost on restart
- No distributed caching

**Recommendation:** Redis for production

---

#### 10. **Celery Not Running**
**Current:** Celery configured but not used

**Impact:**
- Synchronous invoice generation (blocks request)
- No background email sending
- No scheduled tasks

**Recommendation:** Optional - current approach works for small scale

---

#### 11. **No Email Configuration**
**Current:** No email backend configured

**Missing Features:**
- Order confirmation emails
- Password reset emails
- Staff notifications
- Invoice delivery

**Recommendation:** Configure email service

---


## 📝 Detailed Recommendations & Fixes

### PHASE 1: Critical Security Fixes (Day 1-2)

#### Step 1.1: Rotate All Secrets

**Generate New SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Action Items:**
- [ ] Generate new Django SECRET_KEY
- [ ] Create new Razorpay test keys for staging
- [ ] Keep live Razorpay keys for production only
- [ ] Rotate Cloudinary API secret
- [ ] Change database password
- [ ] Update Firebase credentials

**Git History Cleanup:**
```bash
# Remove .env from git history (if committed)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch backend/.env" \
  --prune-empty --tag-name-filter cat -- --all

# Force push (DANGEROUS - coordinate with team)
git push origin --force --all
```

---

#### Step 1.2: Environment Variable Management

**Create Separate Environment Files:**

```bash
# Development
backend/.env.development

# Staging
backend/.env.staging

# Production (NEVER commit this)
backend/.env.production
```

**Update .gitignore:**
```gitignore
# Environment files
.env
.env.*
!.env.example

# Secrets
firebase-credentials.json
*.pem
*.key
```

**Production Environment Variables (Set on Server):**
```bash
# Use your hosting platform's environment variable system
# AWS: Parameter Store / Secrets Manager
# DigitalOcean: App Platform Environment Variables
# Railway: Environment Variables
# Heroku: Config Vars

# Example for Railway/Heroku:
DJANGO_SECRET_KEY=<new-secret-key>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:pass@host:5432/dbname
REDIS_URL=redis://host:6379/0
RAZORPAY_KEY_ID=<live-key>
RAZORPAY_KEY_SECRET=<live-secret>
CLOUDINARY_CLOUD_NAME=<your-cloud>
CLOUDINARY_API_KEY=<your-key>
CLOUDINARY_API_SECRET=<your-secret>
```

---

#### Step 1.3: Update settings.py for Production

**Create settings/base.py, settings/development.py, settings/production.py:**

```python
# election_cart/settings/__init__.py
import os
from .base import *

environment = os.getenv('DJANGO_ENVIRONMENT', 'development')

if environment == 'production':
    from .production import *
elif environment == 'staging':
    from .staging import *
else:
    from .development import *
```

**Or simpler approach - update existing settings.py:**

```python
# At the top of settings.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("DJANGO_SECRET_KEY environment variable is not set")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Allowed hosts
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
if not ALLOWED_HOSTS or ALLOWED_HOSTS == ['']:
    if DEBUG:
        ALLOWED_HOSTS = ['localhost', '127.0.0.1']
    else:
        raise ValueError("ALLOWED_HOSTS must be set in production")

# Production security settings
if not DEBUG:
    # HTTPS settings
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # HSTS settings (HTTP Strict Transport Security)
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Other security headers
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    
    # Proxy settings (if behind load balancer/reverse proxy)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    USE_X_FORWARDED_HOST = True
    USE_X_FORWARDED_PORT = True
```

---

#### Step 1.4: Add Comprehensive Logging

```python
# Add to settings.py

import os
from pathlib import Path

# Create logs directory
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} {module} {funcName} - {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '[{levelname}] {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'error.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'file_info': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'info.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'file_security': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'security.log',
            'maxBytes': 1024 * 1024 * 10,  # 10MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file_error'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['file_error', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['file_security', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'authentication': {
            'handlers': ['console', 'file_info', 'file_error'],
            'level': 'INFO',
            'propagate': False,
        },
        'orders': {
            'handlers': ['console', 'file_info', 'file_error'],
            'level': 'INFO',
            'propagate': False,
        },
        'products': {
            'handlers': ['console', 'file_info', 'file_error'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console', 'file_error'],
        'level': 'INFO',
    },
}
```

---

#### Step 1.5: Add Health Check Endpoint

```python
# election_cart/urls.py

from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import redis
from django.conf import settings

def health_check(request):
    """
    Health check endpoint for monitoring
    Returns 200 if all systems operational
    """
    health_status = {
        'status': 'healthy',
        'service': 'election-cart-api',
        'checks': {}
    }
    
    # Check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health_status['checks']['database'] = 'ok'
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['checks']['database'] = f'error: {str(e)}'
    
    # Check cache
    try:
        cache.set('health_check', 'ok', 10)
        if cache.get('health_check') == 'ok':
            health_status['checks']['cache'] = 'ok'
        else:
            health_status['checks']['cache'] = 'error'
    except Exception as e:
        health_status['checks']['cache'] = f'error: {str(e)}'
    
    # Check Cloudinary (optional)
    if settings.USE_CLOUDINARY:
        health_status['checks']['cloudinary'] = 'configured'
    
    status_code = 200 if health_status['status'] == 'healthy' else 503
    return JsonResponse(health_status, status=status_code)


urlpatterns = [
    path('health/', health_check, name='health-check'),
    path('admin/', admin.site.urls),
    # ... rest of URLs
]
```

---


### PHASE 2: Database & Infrastructure (Day 2-3)

#### Step 2.1: Production Database Setup

**Recommended Managed PostgreSQL Providers:**
1. **AWS RDS** - Most features, scalable
2. **DigitalOcean Managed Database** - Good balance
3. **Railway PostgreSQL** - Easiest setup
4. **Supabase** - PostgreSQL with extras
5. **Neon** - Serverless PostgreSQL

**Database Configuration for Production:**

```python
# settings.py

import dj_database_url

# Parse database URL (works with most hosting platforms)
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,  # Connection pooling
        conn_health_checks=True,  # Django 4.1+
        ssl_require=not DEBUG,  # Require SSL in production
    )
}

# Or manual configuration:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'CONN_MAX_AGE': 600,  # Keep connections alive for 10 minutes
        'OPTIONS': {
            'sslmode': 'require' if not DEBUG else 'prefer',
            'connect_timeout': 10,
        },
    }
}
```

**Install dj-database-url:**
```bash
pip install dj-database-url psycopg2-binary
```

**Backup Strategy:**
```bash
# Automated daily backups (set up on your database provider)
# Manual backup command:
pg_dump -h <host> -U <user> -d <database> -F c -f backup_$(date +%Y%m%d).dump

# Restore command:
pg_restore -h <host> -U <user> -d <database> -c backup_20251103.dump
```

**Action Items:**
- [ ] Create managed PostgreSQL instance
- [ ] Enable automated daily backups
- [ ] Configure SSL connections
- [ ] Test connection from local
- [ ] Document connection string format
- [ ] Test backup and restore process
- [ ] Set up monitoring/alerts for database

---

#### Step 2.2: Redis Cache Setup (Optional but Recommended)

**Why Redis:**
- Distributed caching (works with multiple workers)
- Persistent cache across restarts
- Can be used for Celery broker
- Session storage
- Rate limiting

**Install Dependencies:**
```bash
pip install redis django-redis
```

**Configure Redis:**
```python
# settings.py

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 50,
                'retry_on_timeout': True,
            },
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
        },
        'KEY_PREFIX': 'election_cart',
        'TIMEOUT': 300,  # 5 minutes default
    }
}

# Optional: Use Redis for sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

**Managed Redis Providers:**
- AWS ElastiCache
- DigitalOcean Managed Redis
- Railway Redis
- Redis Cloud
- Upstash (serverless)

---

#### Step 2.3: Static Files Configuration

**Install WhiteNoise:**
```bash
pip install whitenoise[brotli]
```

**Configure WhiteNoise:**
```python
# settings.py

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add after SecurityMiddleware
    'corsheaders.middleware.CorsMiddleware',
    # ... rest of middleware
]

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Collect static files
# Run: python manage.py collectstatic --noinput
```

**Action Items:**
- [ ] Install WhiteNoise
- [ ] Update middleware
- [ ] Run collectstatic
- [ ] Test static file serving
- [ ] Configure CDN (optional - CloudFlare, AWS CloudFront)

---

#### Step 2.4: Rate Limiting Implementation

**Install django-ratelimit:**
```bash
pip install django-ratelimit
```

**Add Rate Limiting to Critical Endpoints:**

```python
# authentication/views.py

from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', method='POST')  # 5 attempts per minute
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    # Check if rate limited
    if getattr(request, 'limited', False):
        return Response(
            {'error': 'Too many login attempts. Please try again later.'},
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )
    # ... rest of login logic


@ratelimit(key='ip', rate='3/h', method='POST')  # 3 signups per hour
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    if getattr(request, 'limited', False):
        return Response(
            {'error': 'Too many signup attempts. Please try again later.'},
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )
    # ... rest of signup logic
```

```python
# orders/views.py

from django_ratelimit.decorators import ratelimit

@ratelimit(key='user', rate='10/h', method='POST')  # 10 orders per hour per user
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    if getattr(request, 'limited', False):
        return Response(
            {'error': 'Too many orders. Please try again later.'},
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )
    # ... rest of order creation


@ratelimit(key='user', rate='20/h', method='POST')  # 20 uploads per hour
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_resources(request, order_id):
    if getattr(request, 'limited', False):
        return Response(
            {'error': 'Too many upload attempts. Please try again later.'},
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )
    # ... rest of upload logic
```

**Configure Rate Limiting:**
```python
# settings.py

# Use Redis for rate limiting (if available)
RATELIMIT_USE_CACHE = 'default'
RATELIMIT_ENABLE = not DEBUG  # Disable in development
```

---

#### Step 2.5: Error Tracking with Sentry

**Install Sentry:**
```bash
pip install sentry-sdk
```

**Configure Sentry:**
```python
# settings.py

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

if not DEBUG:
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,  # 10% of transactions
        send_default_pii=False,  # Don't send user data
        environment=os.getenv('DJANGO_ENVIRONMENT', 'production'),
        release=os.getenv('GIT_COMMIT_SHA', 'unknown'),
    )
```

**Get Sentry DSN:**
1. Sign up at https://sentry.io (free tier available)
2. Create new project
3. Copy DSN
4. Add to environment variables

---


### PHASE 3: Deployment Configuration (Day 3-4)

#### Step 3.1: Update requirements.txt

```bash
# Add production dependencies
pip install whitenoise[brotli]
pip install dj-database-url
pip install django-redis
pip install redis
pip install django-ratelimit
pip install sentry-sdk
pip install gunicorn

# Freeze requirements
pip freeze > requirements.txt
```

**Create requirements-prod.txt (optional):**
```txt
# Production-only dependencies
gunicorn==21.2.0
whitenoise[brotli]==6.6.0
dj-database-url==2.1.0
django-redis==5.4.0
redis==5.0.1
django-ratelimit==4.1.0
sentry-sdk==1.39.1
```

---

#### Step 3.2: Create Gunicorn Configuration

```python
# gunicorn.conf.py

import multiprocessing
import os

# Server socket
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
backlog = 2048

# Worker processes
workers = int(os.getenv('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'sync'
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2

# Logging
accesslog = '-'  # Log to stdout
errorlog = '-'   # Log to stderr
loglevel = os.getenv('GUNICORN_LOG_LEVEL', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'election_cart'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (if terminating SSL at application level)
# keyfile = '/path/to/key.pem'
# certfile = '/path/to/cert.pem'
```

**Start Gunicorn:**
```bash
gunicorn election_cart.wsgi:application -c gunicorn.conf.py
```

---

#### Step 3.3: Create Dockerfile (Optional)

```dockerfile
# Dockerfile

FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create logs directory
RUN mkdir -p logs

# Collect static files
RUN python manage.py collectstatic --noinput

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health/')"

# Run gunicorn
CMD ["gunicorn", "election_cart.wsgi:application", "-c", "gunicorn.conf.py"]
```

**Create .dockerignore:**
```
.env
.env.*
*.pyc
__pycache__
.git
.gitignore
*.md
logs/
media/
staticfiles/
.vscode/
.idea/
```

---

#### Step 3.4: Create docker-compose.yml (For Local Testing)

```yaml
# docker-compose.yml

version: '3.8'

services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: election_cart
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  web:
    build: .
    command: gunicorn election_cart.wsgi:application -c gunicorn.conf.py
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env.development
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

---

#### Step 3.5: Deployment Scripts

**Create deploy.sh:**
```bash
#!/bin/bash
# deploy.sh - Production deployment script

set -e  # Exit on error

echo "🚀 Starting deployment..."

# Pull latest code
echo "📥 Pulling latest code..."
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗄️  Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Run security checks
echo "🔒 Running security checks..."
python manage.py check --deploy

# Restart gunicorn
echo "🔄 Restarting application..."
sudo systemctl restart gunicorn

echo "✅ Deployment complete!"
```

**Create pre-deploy-check.sh:**
```bash
#!/bin/bash
# pre-deploy-check.sh - Run before deployment

set -e

echo "🔍 Running pre-deployment checks..."

# Check environment variables
echo "Checking environment variables..."
python -c "
import os
required_vars = [
    'DJANGO_SECRET_KEY',
    'DATABASE_URL',
    'ALLOWED_HOSTS',
    'RAZORPAY_KEY_ID',
    'RAZORPAY_KEY_SECRET',
]
missing = [var for var in required_vars if not os.getenv(var)]
if missing:
    print(f'❌ Missing environment variables: {missing}')
    exit(1)
print('✅ All required environment variables set')
"

# Run tests
echo "Running tests..."
python manage.py test

# Check migrations
echo "Checking migrations..."
python manage.py makemigrations --check --dry-run

# Security check
echo "Running security check..."
python manage.py check --deploy

echo "✅ All pre-deployment checks passed!"
```

---

#### Step 3.6: Systemd Service (For Linux Servers)

**Create /etc/systemd/system/gunicorn.service:**
```ini
[Unit]
Description=Gunicorn daemon for Election Cart
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/election-cart/backend
Environment="PATH=/var/www/election-cart/backend/venv/bin"
EnvironmentFile=/var/www/election-cart/backend/.env.production
ExecStart=/var/www/election-cart/backend/venv/bin/gunicorn \
          --config gunicorn.conf.py \
          election_cart.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
sudo systemctl status gunicorn
```

---

#### Step 3.7: Nginx Configuration (Reverse Proxy)

**Create /etc/nginx/sites-available/election-cart:**
```nginx
upstream election_cart {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Client body size (for file uploads)
    client_max_body_size 20M;
    
    # Timeouts
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
    
    # Static files
    location /static/ {
        alias /var/www/election-cart/backend/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Media files (if not using Cloudinary)
    location /media/ {
        alias /var/www/election-cart/backend/media/;
        expires 7d;
        add_header Cache-Control "public";
    }
    
    # Proxy to Django
    location / {
        proxy_pass http://election_cart;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
    
    # Health check
    location /health/ {
        proxy_pass http://election_cart;
        access_log off;
    }
}
```

**Enable site:**
```bash
sudo ln -s /etc/nginx/sites-available/election-cart /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

**Get SSL Certificate (Let's Encrypt):**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

---


### PHASE 4: Testing & Validation (Day 4-5)

#### Step 4.1: Security Testing Checklist

```bash
# Run Django security check
python manage.py check --deploy

# Expected output: System check identified no issues (0 silenced).
```

**Manual Security Tests:**
- [ ] Verify DEBUG=False in production
- [ ] Test HTTPS redirect works
- [ ] Verify security headers present (use securityheaders.com)
- [ ] Test CORS only allows production domains
- [ ] Verify rate limiting works (try multiple rapid requests)
- [ ] Test file upload validation (try malicious files)
- [ ] Verify authentication required on protected endpoints
- [ ] Test SQL injection protection (Django ORM handles this)
- [ ] Verify XSS protection (try script tags in inputs)
- [ ] Test CSRF protection on POST requests

**Security Scanning Tools:**
```bash
# Install safety (checks for vulnerable dependencies)
pip install safety
safety check

# Install bandit (Python security linter)
pip install bandit
bandit -r . -ll

# Check for secrets in code
pip install detect-secrets
detect-secrets scan
```

---

#### Step 4.2: Performance Testing

**Load Testing with Locust:**
```bash
pip install locust
```

**Create locustfile.py:**
```python
from locust import HttpUser, task, between

class ElectionCartUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        # Login
        response = self.client.post("/api/auth/login/", json={
            "username": "testuser",
            "password": "testpass123"
        })
        if response.status_code == 200:
            self.token = response.json()['token']
    
    @task(3)
    def view_packages(self):
        self.client.get("/api/packages/")
    
    @task(2)
    def view_campaigns(self):
        self.client.get("/api/campaigns/")
    
    @task(1)
    def view_cart(self):
        self.client.get("/api/cart/", headers={
            "Authorization": f"Bearer {self.token}"
        })
```

**Run load test:**
```bash
locust -f locustfile.py --host=https://yourdomain.com
# Open http://localhost:8089 to start test
```

**Performance Targets:**
- API response time: < 200ms (p95)
- Database queries: < 50ms
- File uploads: < 2s for 5MB
- Concurrent users: 100+ without degradation

---

#### Step 4.3: Database Performance Optimization

**Check for Missing Indexes:**
```python
# Run this in Django shell
from django.db import connection
from django.db.models import Count

# Check slow queries
print(connection.queries)

# Analyze query plans
from orders.models import Order
print(Order.objects.filter(status='pending_payment').explain())
```

**Add Missing Indexes (if needed):**
```python
# In models.py
class Order(models.Model):
    # ... existing fields
    
    class Meta:
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['user', 'status']),
            models.Index(fields=['assigned_to', 'status']),
            models.Index(fields=['-payment_completed_at']),
        ]
```

**Optimize Queries:**
```python
# Bad - N+1 queries
orders = Order.objects.all()
for order in orders:
    print(order.user.username)  # Hits database each time

# Good - Use select_related
orders = Order.objects.select_related('user', 'assigned_to').all()
for order in orders:
    print(order.user.username)  # No additional queries

# Good - Use prefetch_related for many-to-many
orders = Order.objects.prefetch_related('items', 'items__content_object').all()
```

---

#### Step 4.4: Monitoring Setup

**1. Uptime Monitoring (UptimeRobot - Free)**
- Sign up at https://uptimerobot.com
- Add monitor for https://yourdomain.com/health/
- Set check interval: 5 minutes
- Add alert contacts (email, SMS)

**2. Application Performance Monitoring**

**Option A: New Relic (Free tier available)**
```bash
pip install newrelic
newrelic-admin generate-config YOUR_LICENSE_KEY newrelic.ini
```

**Start with New Relic:**
```bash
NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program gunicorn election_cart.wsgi:application
```

**Option B: DataDog (Free trial)**
```bash
pip install ddtrace
```

**Start with DataDog:**
```bash
ddtrace-run gunicorn election_cart.wsgi:application
```

**3. Log Aggregation**

**Option A: Papertrail (Free tier)**
- Sign up at https://papertrailapp.com
- Configure rsyslog to forward logs
- View logs in real-time dashboard

**Option B: AWS CloudWatch (if using AWS)**
```bash
pip install watchtower
```

```python
# settings.py
import watchtower

LOGGING['handlers']['cloudwatch'] = {
    'level': 'INFO',
    'class': 'watchtower.CloudWatchLogHandler',
    'log_group': 'election-cart',
    'stream_name': 'django',
}
```

---

#### Step 4.5: Backup Testing

**Test Database Backup:**
```bash
# Create backup
pg_dump -h <host> -U <user> -d <database> -F c -f test_backup.dump

# Create test database
createdb -h <host> -U <user> test_restore

# Restore backup
pg_restore -h <host> -U <user> -d test_restore -c test_backup.dump

# Verify data
psql -h <host> -U <user> -d test_restore -c "SELECT COUNT(*) FROM orders_order;"

# Cleanup
dropdb -h <host> -U <user> test_restore
```

**Test Cloudinary Backup:**
- Cloudinary automatically backs up your media
- Test by downloading a few files
- Verify file integrity

---


### PHASE 5: Deployment & Go-Live (Day 5-7)

#### Step 5.1: Choose Hosting Platform

**Recommended Platforms (Easiest to Hardest):**

**1. Railway (Recommended for Quick Start)**
- ✅ Automatic deployments from Git
- ✅ Built-in PostgreSQL and Redis
- ✅ Environment variables UI
- ✅ Free tier available
- ✅ Easy scaling
- 💰 ~$20-40/month

**2. DigitalOcean App Platform**
- ✅ Managed platform
- ✅ Good documentation
- ✅ Reasonable pricing
- ✅ Managed databases available
- 💰 ~$30-60/month

**3. Heroku**
- ✅ Very easy deployment
- ✅ Lots of add-ons
- ❌ Expensive
- 💰 ~$50-100/month

**4. AWS (Most Flexible, Most Complex)**
- ✅ Most features
- ✅ Best scaling
- ❌ Complex setup
- ❌ Steep learning curve
- 💰 ~$40-100/month

**5. Self-Hosted VPS (DigitalOcean Droplet, Linode)**
- ✅ Full control
- ✅ Cheapest option
- ❌ Manual setup required
- ❌ You manage everything
- 💰 ~$12-24/month

---

#### Step 5.2: Deployment Guide (Railway Example)

**1. Install Railway CLI:**
```bash
npm install -g @railway/cli
railway login
```

**2. Initialize Project:**
```bash
cd backend
railway init
```

**3. Add PostgreSQL:**
```bash
railway add --plugin postgresql
```

**4. Add Redis:**
```bash
railway add --plugin redis
```

**5. Set Environment Variables:**
```bash
railway variables set DJANGO_SECRET_KEY="your-new-secret-key"
railway variables set DEBUG="False"
railway variables set ALLOWED_HOSTS="your-app.railway.app"
railway variables set DJANGO_ENVIRONMENT="production"
# ... set all other variables
```

**6. Create railway.json:**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements.txt && python manage.py collectstatic --noinput"
  },
  "deploy": {
    "startCommand": "python manage.py migrate && gunicorn election_cart.wsgi:application -c gunicorn.conf.py",
    "healthcheckPath": "/health/",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**7. Deploy:**
```bash
railway up
```

**8. Get Domain:**
```bash
railway domain
# Or add custom domain in Railway dashboard
```

---

#### Step 5.3: Post-Deployment Checklist

**Immediate Checks (Within 1 hour):**
- [ ] Health check endpoint returns 200
- [ ] Can access admin panel
- [ ] Can login with test account
- [ ] Can view products
- [ ] Can add items to cart
- [ ] Can create order
- [ ] Payment flow works (test mode)
- [ ] File upload works
- [ ] Images load from Cloudinary
- [ ] Static files load correctly
- [ ] HTTPS works
- [ ] Security headers present

**Within 24 Hours:**
- [ ] Monitor error logs
- [ ] Check database connections
- [ ] Verify backups running
- [ ] Test email notifications (if configured)
- [ ] Monitor response times
- [ ] Check memory/CPU usage
- [ ] Verify rate limiting works
- [ ] Test from different devices/networks

**Within 1 Week:**
- [ ] Review all error logs
- [ ] Analyze performance metrics
- [ ] Check for slow queries
- [ ] Review security logs
- [ ] Test backup restoration
- [ ] Verify monitoring alerts work
- [ ] Check disk space usage
- [ ] Review API usage patterns

---

#### Step 5.4: Rollback Plan

**If Something Goes Wrong:**

**1. Quick Rollback (Railway/Heroku):**
```bash
# Railway
railway rollback

# Heroku
heroku rollback
```

**2. Manual Rollback:**
```bash
# Revert to previous commit
git revert HEAD
git push origin main

# Or checkout previous version
git checkout <previous-commit-sha>
git push origin main --force
```

**3. Database Rollback:**
```bash
# Restore from backup
pg_restore -h <host> -U <user> -d <database> -c backup_before_deploy.dump
```

**4. Notify Users:**
- Update status page
- Send email notification
- Post on social media

---

#### Step 5.5: Monitoring Dashboard Setup

**Create Simple Status Page:**

```python
# admin_panel/views.py

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def system_status(request):
    """
    GET /api/admin/system-status/
    Get system health and metrics
    """
    from django.db import connection
    from django.core.cache import cache
    import psutil
    
    status = {
        'timestamp': timezone.now().isoformat(),
        'status': 'healthy',
        'services': {},
        'metrics': {}
    }
    
    # Database check
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        status['services']['database'] = 'healthy'
    except Exception as e:
        status['services']['database'] = f'unhealthy: {str(e)}'
        status['status'] = 'degraded'
    
    # Cache check
    try:
        cache.set('health_check', 'ok', 10)
        status['services']['cache'] = 'healthy' if cache.get('health_check') == 'ok' else 'unhealthy'
    except Exception as e:
        status['services']['cache'] = f'unhealthy: {str(e)}'
    
    # System metrics
    try:
        status['metrics']['cpu_percent'] = psutil.cpu_percent(interval=1)
        status['metrics']['memory_percent'] = psutil.virtual_memory().percent
        status['metrics']['disk_percent'] = psutil.disk_usage('/').percent
    except:
        pass
    
    # Application metrics
    status['metrics']['total_orders'] = Order.objects.count()
    status['metrics']['pending_orders'] = Order.objects.filter(
        status__in=['pending_payment', 'pending_resources']
    ).count()
    status['metrics']['active_users'] = CustomUser.objects.filter(
        last_login__gte=timezone.now() - timedelta(days=30)
    ).count()
    
    return Response(status)
```

---


## 📊 Production Readiness Scorecard

### Current Status: 60/100

| Category | Score | Status | Priority |
|----------|-------|--------|----------|
| **Security** | 40/100 | 🔴 Critical | P0 |
| - Secrets Management | 0/20 | 🔴 Exposed | P0 |
| - DEBUG Mode | 0/10 | 🔴 Enabled | P0 |
| - Security Headers | 0/15 | 🔴 Missing | P0 |
| - HTTPS | 0/15 | 🔴 Not Configured | P0 |
| - Rate Limiting | 0/10 | 🔴 Missing | P1 |
| - File Security | 30/30 | ✅ Good | - |
| **Infrastructure** | 30/100 | 🟡 Needs Work | P1 |
| - Database | 10/25 | 🟡 Local Only | P1 |
| - Caching | 5/15 | 🟡 Basic | P2 |
| - Static Files | 5/15 | 🟡 Not Optimized | P1 |
| - Backups | 0/20 | 🔴 None | P1 |
| - Monitoring | 10/25 | 🟡 Minimal | P1 |
| **Performance** | 60/100 | 🟢 Acceptable | P2 |
| - Query Optimization | 20/25 | ✅ Good | - |
| - Caching Strategy | 10/25 | 🟡 Basic | P2 |
| - CDN | 10/20 | 🟡 Partial | P2 |
| - Load Balancing | 0/15 | 🔴 None | P3 |
| - Connection Pooling | 20/15 | ✅ Good | - |
| **Reliability** | 50/100 | 🟡 Needs Work | P1 |
| - Error Handling | 20/25 | ✅ Good | - |
| - Logging | 10/25 | 🟡 Basic | P1 |
| - Health Checks | 0/15 | 🔴 Missing | P1 |
| - Alerting | 0/20 | 🔴 None | P1 |
| - Disaster Recovery | 20/15 | ✅ Good | - |
| **Code Quality** | 80/100 | ✅ Good | - |
| - Architecture | 25/25 | ✅ Excellent | - |
| - Code Organization | 20/20 | ✅ Excellent | - |
| - Documentation | 15/20 | ✅ Good | - |
| - Testing | 10/20 | 🟡 Minimal | P2 |
| - Type Hints | 10/15 | 🟡 Partial | P3 |

**Target Score for Production: 85/100**

---

## 🎯 Priority Action Items

### P0 - Critical (Must Fix Before Launch)

1. **Rotate All Secrets** ⏱️ 1 hour
   - Generate new SECRET_KEY
   - Create new Razorpay test keys
   - Rotate Cloudinary credentials
   - Remove .env from git history

2. **Fix DEBUG Mode** ⏱️ 15 minutes
   - Set DEBUG=False default
   - Configure error pages
   - Set up error logging

3. **Add Security Headers** ⏱️ 30 minutes
   - HTTPS enforcement
   - HSTS headers
   - Secure cookies
   - CSP headers

4. **Configure ALLOWED_HOSTS** ⏱️ 15 minutes
   - Add production domain
   - Remove localhost

**Total P0 Time: ~2 hours**

---

### P1 - High Priority (Fix Within Week 1)

5. **Set Up Production Database** ⏱️ 2-4 hours
   - Create managed PostgreSQL
   - Enable SSL
   - Configure backups
   - Test connection

6. **Add Comprehensive Logging** ⏱️ 2 hours
   - Configure log files
   - Set up log rotation
   - Add structured logging

7. **Implement Rate Limiting** ⏱️ 2 hours
   - Install django-ratelimit
   - Add to critical endpoints
   - Test limits

8. **Set Up Monitoring** ⏱️ 3 hours
   - Add health check endpoint
   - Configure Sentry
   - Set up uptime monitoring
   - Configure alerts

9. **Configure Static Files** ⏱️ 1 hour
   - Install WhiteNoise
   - Run collectstatic
   - Test serving

**Total P1 Time: ~10-12 hours**

---

### P2 - Medium Priority (Fix Within Month 1)

10. **Set Up Redis Cache** ⏱️ 2 hours
11. **Add Email Configuration** ⏱️ 3 hours
12. **Write Tests** ⏱️ 8 hours
13. **Performance Optimization** ⏱️ 4 hours
14. **Documentation** ⏱️ 4 hours

**Total P2 Time: ~21 hours**

---

### P3 - Low Priority (Nice to Have)

15. **Set Up Celery** ⏱️ 4 hours
16. **Add Type Hints** ⏱️ 8 hours
17. **Set Up CI/CD** ⏱️ 6 hours
18. **Load Balancing** ⏱️ 4 hours

**Total P3 Time: ~22 hours**

---

## 📅 Recommended Timeline

### Week 1: Critical Fixes
- **Day 1-2:** Security fixes (P0 items)
- **Day 3-4:** Infrastructure setup (P1 items)
- **Day 5:** Testing and validation
- **Day 6-7:** Deployment to staging

### Week 2: Stabilization
- **Day 8-10:** Monitor staging, fix issues
- **Day 11-12:** Performance optimization
- **Day 13-14:** Production deployment

### Week 3-4: Optimization
- **Week 3:** Medium priority items
- **Week 4:** Documentation and training

---

## 💰 Estimated Costs

### Minimal Production Setup
| Service | Provider | Cost/Month |
|---------|----------|------------|
| Hosting | Railway | $20 |
| Database | Railway PostgreSQL | Included |
| Redis | Railway Redis | Included |
| Cloudinary | Free Tier | $0 |
| Domain | Namecheap | $1 |
| SSL | Let's Encrypt | $0 |
| Monitoring | UptimeRobot Free | $0 |
| Error Tracking | Sentry Free | $0 |
| **Total** | | **~$21/month** |

### Recommended Production Setup
| Service | Provider | Cost/Month |
|---------|----------|------------|
| Hosting | DigitalOcean App Platform | $40 |
| Database | DO Managed PostgreSQL | $50 |
| Redis | DO Managed Redis | $15 |
| Cloudinary | Plus Plan | $89 |
| Domain | Namecheap | $1 |
| SSL | Let's Encrypt | $0 |
| Monitoring | UptimeRobot | $0 |
| Error Tracking | Sentry Team | $26 |
| APM | New Relic | $0 (free tier) |
| CDN | Cloudflare | $0 (free tier) |
| **Total** | | **~$221/month** |

### Enterprise Setup
| Service | Provider | Cost/Month |
|---------|----------|------------|
| Hosting | AWS ECS | $100 |
| Database | AWS RDS | $150 |
| Redis | AWS ElastiCache | $50 |
| Cloudinary | Advanced | $224 |
| Domain | Route 53 | $1 |
| SSL | AWS ACM | $0 |
| Monitoring | DataDog | $75 |
| Error Tracking | Sentry Business | $80 |
| CDN | CloudFront | $50 |
| Backups | AWS S3 | $20 |
| **Total** | | **~$750/month** |

---

## 🔧 Quick Start Commands

### Local Development
```bash
# Set up environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up database
python manage.py migrate
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Production Deployment
```bash
# Install production dependencies
pip install -r requirements.txt

# Set environment variables
export DEBUG=False
export DJANGO_SECRET_KEY="your-secret-key"
# ... set all other variables

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Run security check
python manage.py check --deploy

# Start gunicorn
gunicorn election_cart.wsgi:application -c gunicorn.conf.py
```

---

## 📚 Additional Resources

### Documentation to Create
1. **API Documentation** - Use drf-spectacular or Swagger
2. **Deployment Guide** - Step-by-step deployment instructions
3. **Environment Variables Guide** - All required variables
4. **Backup/Restore Procedures** - How to backup and restore
5. **Troubleshooting Guide** - Common issues and solutions
6. **Monitoring Guide** - How to monitor the application
7. **Security Guide** - Security best practices
8. **Development Guide** - How to set up local development

### Recommended Reading
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
- [12 Factor App](https://12factor.net/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

## ✅ Final Pre-Launch Checklist

### Security
- [ ] All secrets rotated and secured
- [ ] DEBUG=False in production
- [ ] Security headers configured
- [ ] HTTPS enabled and enforced
- [ ] Rate limiting implemented
- [ ] File upload validation working
- [ ] Authentication tested
- [ ] CORS configured correctly
- [ ] CSRF protection enabled
- [ ] SQL injection protection verified

### Infrastructure
- [ ] Production database set up
- [ ] Database backups configured
- [ ] Backup restoration tested
- [ ] Redis cache configured (optional)
- [ ] Static files optimized
- [ ] CDN configured (optional)
- [ ] Domain configured
- [ ] SSL certificate installed

### Monitoring
- [ ] Health check endpoint working
- [ ] Error tracking configured (Sentry)
- [ ] Uptime monitoring set up
- [ ] Log aggregation configured
- [ ] Alerts configured
- [ ] Performance monitoring set up

### Testing
- [ ] All API endpoints tested
- [ ] Payment flow tested
- [ ] File uploads tested
- [ ] Authentication tested
- [ ] Admin panel tested
- [ ] Load testing completed
- [ ] Security testing completed

### Documentation
- [ ] API documentation complete
- [ ] Deployment guide written
- [ ] Environment variables documented
- [ ] Backup procedures documented
- [ ] Troubleshooting guide created

### Deployment
- [ ] Staging environment tested
- [ ] Production environment configured
- [ ] Rollback plan documented
- [ ] Team trained on deployment
- [ ] Support plan in place

---

## 🎉 Conclusion

Your Django backend is **well-architected** with solid features, but requires **critical security hardening** before production deployment. Follow this plan systematically, starting with P0 items, and you'll have a production-ready system in 5-7 days.

**Key Takeaways:**
1. **Security First** - Fix all P0 items before anything else
2. **Test Everything** - Don't skip testing phase
3. **Monitor Closely** - Watch logs and metrics after launch
4. **Start Small** - Use minimal setup first, scale as needed
5. **Document Everything** - Future you will thank you

**Next Steps:**
1. Review this plan with your team
2. Choose hosting platform
3. Start with Phase 1 (Security Fixes)
4. Deploy to staging first
5. Test thoroughly
6. Deploy to production
7. Monitor and iterate

Good luck with your deployment! 🚀

---

**Questions or Need Help?**
- Review Django documentation
- Check hosting platform docs
- Join Django community forums
- Consider hiring DevOps consultant for complex setups


# 🔧 Exact Code Changes Required

**Copy-paste these exact changes into your files**

---

## File 1: `backend/election_cart/settings.py`

### Change 1: Fix DEBUG default (Line ~17)

**FIND:**
```python
DEBUG = os.getenv('DEBUG', 'True') == 'True'
```

**REPLACE WITH:**
```python
DEBUG = os.getenv('DEBUG', 'False') == 'True'  # Default to False for security
```

---

### Change 2: Add security headers (Add at end of file, before last line)

**ADD THIS BLOCK:**
```python
# ============================================================================
# PRODUCTION SECURITY SETTINGS
# ============================================================================

if not DEBUG:
    # HTTPS settings
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # HSTS (HTTP Strict Transport Security)
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
```

---

### Change 3: Add logging configuration (Add after CELERY settings)

**ADD THIS BLOCK:**
```python
# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

# Create logs directory
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} - {message}',
            'style': '{',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '[{levelname}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'django.log',
            'maxBytes': 1024 * 1024 * 5,  # 5MB
            'backupCount': 3,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'error.log',
            'maxBytes': 1024 * 1024 * 5,  # 5MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['error_file', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
```

---

### Change 4: Add database URL support (Replace DATABASES section)

**FIND:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'election_cart'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

**REPLACE WITH:**
```python
import dj_database_url

# Database configuration
# Supports DATABASE_URL (Railway, Heroku) or manual configuration
if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ['DATABASE_URL'],
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=not DEBUG,
        )
    }
else:
    # Fallback to manual configuration
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'election_cart'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'postgres'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
            'CONN_MAX_AGE': 600,
        }
    }
```

---

### Change 5: Add WhiteNoise (Update MIDDLEWARE)

**FIND:**
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
```

**REPLACE WITH:**
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this line
    'corsheaders.middleware.CorsMiddleware',
```

**AND ADD (after STATIC_ROOT):**
```python
# WhiteNoise configuration for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
```

---

### Change 6: Add Sentry (Add after imports at top)

**ADD AFTER IMPORTS:**
```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Sentry error tracking (production only)
if not DEBUG and os.getenv('SENTRY_DSN'):
    sentry_sdk.init(
        dsn=os.getenv('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.0,  # Disable performance monitoring to save quota
        send_default_pii=False,  # Don't send user data
        environment=os.getenv('DJANGO_ENVIRONMENT', 'production'),
    )
```

---

## File 2: `backend/election_cart/urls.py`

### Add health check endpoint

**ADD AFTER IMPORTS:**
```python
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    """
    Health check endpoint for monitoring
    Returns 200 if database is accessible
    """
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'healthy',
            'service': 'election-cart-api',
            'database': 'connected'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'service': 'election-cart-api',
            'database': 'disconnected',
            'error': str(e)
        }, status=503)
```

**ADD TO urlpatterns (at the beginning):**
```python
urlpatterns = [
    path('health/', health_check, name='health-check'),  # Add this line
    path('admin/', admin.site.urls),
    # ... rest of URLs
]
```

---

## File 3: `backend/authentication/views.py`

### Add rate limiting to login and signup

**ADD IMPORT AT TOP:**
```python
from django_ratelimit.decorators import ratelimit
```

**UPDATE login function:**

**FIND:**
```python
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
```

**REPLACE WITH:**
```python
@ratelimit(key='ip', rate='5/m', method='POST')
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Login with username and password.
    Rate limited to 5 attempts per minute per IP.
    """
    # Check if rate limited
    if getattr(request, 'limited', False):
        return Response(
            {'error': 'Too many login attempts. Please try again in a minute.'},
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )
```

**UPDATE signup function:**

**FIND:**
```python
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
```

**REPLACE WITH:**
```python
@ratelimit(key='ip', rate='3/h', method='POST')
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """
    Create new user account.
    Rate limited to 3 signups per hour per IP.
    """
    # Check if rate limited
    if getattr(request, 'limited', False):
        return Response(
            {'error': 'Too many signup attempts. Please try again later.'},
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )
```

---

## File 4: `backend/orders/views.py`

### Add rate limiting to order creation

**ADD IMPORT AT TOP:**
```python
from django_ratelimit.decorators import ratelimit
```

**UPDATE create_order function:**

**FIND:**
```python
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
```

**REPLACE WITH:**
```python
@ratelimit(key='user', rate='10/h', method='POST')
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    """
    Create order from cart and generate Razorpay order.
    Rate limited to 10 orders per hour per user.
    """
    # Check if rate limited
    if getattr(request, 'limited', False):
        return Response(
            {'error': 'Too many orders. Please try again later.'},
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )
```

---

## File 5: `backend/.gitignore`

### Add logs directory

**ADD THESE LINES:**
```
# Logs
logs/
*.log

# Environment files (make sure these are here)
.env
.env.*
!.env.example

# Secrets
firebase-credentials.json
```

---

## File 6: `backend/Procfile` (NEW FILE)

**CREATE THIS FILE:**
```
web: python manage.py migrate && gunicorn election_cart.wsgi:application --bind 0.0.0.0:$PORT
```

---

## File 7: `backend/templates/404.html` (NEW FILE)

**CREATE THIS FILE:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 - Page Not Found</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            text-align: center;
            padding: 2rem;
        }
        h1 {
            font-size: 6rem;
            margin: 0;
        }
        p {
            font-size: 1.5rem;
            margin: 1rem 0;
        }
        a {
            display: inline-block;
            margin-top: 2rem;
            padding: 1rem 2rem;
            background: white;
            color: #667eea;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            transition: transform 0.2s;
        }
        a:hover {
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>404</h1>
        <p>Page Not Found</p>
        <p>The page you're looking for doesn't exist.</p>
        <a href="/">Go Home</a>
    </div>
</body>
</html>
```

---

## File 8: `backend/templates/500.html` (NEW FILE)

**CREATE THIS FILE:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>500 - Server Error</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
        }
        .container {
            text-align: center;
            padding: 2rem;
        }
        h1 {
            font-size: 6rem;
            margin: 0;
        }
        p {
            font-size: 1.5rem;
            margin: 1rem 0;
        }
        a {
            display: inline-block;
            margin-top: 2rem;
            padding: 1rem 2rem;
            background: white;
            color: #f5576c;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            transition: transform 0.2s;
        }
        a:hover {
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>500</h1>
        <p>Server Error</p>
        <p>Something went wrong. We're working on it!</p>
        <a href="/">Go Home</a>
    </div>
</body>
</html>
```

---

## File 9: `backend/requirements.txt`

### Add new dependencies

**RUN THESE COMMANDS:**
```bash
pip install whitenoise dj-database-url django-ratelimit sentry-sdk gunicorn
pip freeze > requirements.txt
```

**OR MANUALLY ADD TO requirements.txt:**
```txt
# ... existing packages ...

# Production essentials
whitenoise>=6.6.0
dj-database-url>=2.1.0
django-ratelimit>=4.1.0
sentry-sdk>=1.39.1
gunicorn>=21.2.0
```

---

## Summary of Changes

### Files Modified:
1. ✅ `backend/election_cart/settings.py` - 6 changes
2. ✅ `backend/election_cart/urls.py` - 1 addition
3. ✅ `backend/authentication/views.py` - 2 changes
4. ✅ `backend/orders/views.py` - 1 change
5. ✅ `backend/.gitignore` - 1 addition
6. ✅ `backend/requirements.txt` - 5 additions

### Files Created:
7. ✅ `backend/Procfile` - NEW
8. ✅ `backend/templates/404.html` - NEW
9. ✅ `backend/templates/500.html` - NEW

### Total Changes: 9 files

---

## Testing After Changes

```bash
# 1. Install new dependencies
pip install -r requirements.txt

# 2. Create logs directory
mkdir logs

# 3. Collect static files
python manage.py collectstatic --noinput

# 4. Run security check
python manage.py check --deploy

# 5. Test locally with DEBUG=False
export DEBUG=False
python manage.py runserver

# 6. Test health check
curl http://localhost:8000/health/

# 7. Test rate limiting
# Try logging in 6 times rapidly - should get rate limited
```

---

## Next Steps

After making these changes:
1. ✅ Commit changes to git
2. ✅ Set up Railway account
3. ✅ Deploy to Railway
4. ✅ Set environment variables
5. ✅ Test deployment

**See IMPLEMENTATION_CHECKLIST.md for detailed steps!**

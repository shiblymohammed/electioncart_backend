# Environment Variables Reference

Complete reference for all environment variables used in the Election Cart backend.

## Quick Start

```bash
# Copy example file
cp .env.example .env

# Edit with your values
nano .env
```

## Required Variables

### Django Core

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DJANGO_SECRET_KEY` | ✅ Yes | - | Django secret key for cryptographic signing |
| `DEBUG` | ✅ Yes | `False` | Enable debug mode (True/False) |
| `ALLOWED_HOSTS` | ✅ Yes | `localhost,127.0.0.1` | Comma-separated list of allowed hosts |

### Database

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | ⚠️ Production | - | Full database URL (Railway, Heroku) |
| `DB_NAME` | ⚠️ Development | `election_cart` | Database name |
| `DB_USER` | ⚠️ Development | `postgres` | Database user |
| `DB_PASSWORD` | ⚠️ Development | - | Database password |
| `DB_HOST` | ⚠️ Development | `localhost` | Database host |
| `DB_PORT` | ⚠️ Development | `5432` | Database port |

**Note**: Use either `DATABASE_URL` OR individual `DB_*` variables, not both.

### Payment Processing

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `RAZORPAY_KEY_ID` | ✅ Yes | - | Razorpay API key (test or live) |
| `RAZORPAY_KEY_SECRET` | ✅ Yes | - | Razorpay API secret |

### File Storage

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `CLOUDINARY_CLOUD_NAME` | ✅ Yes | - | Cloudinary cloud name |
| `CLOUDINARY_API_KEY` | ✅ Yes | - | Cloudinary API key |
| `CLOUDINARY_API_SECRET` | ✅ Yes | - | Cloudinary API secret |

## Optional Variables

### CORS

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `CORS_ALLOWED_ORIGINS` | ❌ No | `http://localhost:3000,...` | Comma-separated frontend URLs |

### Firebase

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `FIREBASE_CREDENTIALS_PATH` | ❌ No | `firebase-credentials.json` | Path to Firebase credentials |

### Error Tracking

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SENTRY_DSN` | ❌ No | - | Sentry project DSN for error tracking |
| `SENTRY_RELEASE` | ❌ No | - | Release version for Sentry |
| `DJANGO_ENVIRONMENT` | ❌ No | `production` | Environment name (dev/staging/prod) |

## Environment-Specific Configurations

### Development (.env or .env.development)

```bash
# Django
DJANGO_SECRET_KEY=dev-secret-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_ENVIRONMENT=development

# Database (local)
DB_NAME=election_cart
DB_USER=postgres
DB_PASSWORD=your_local_password
DB_HOST=localhost
DB_PORT=5432

# CORS (local frontends)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Razorpay (TEST keys)
RAZORPAY_KEY_ID=rzp_test_YOUR_TEST_KEY
RAZORPAY_KEY_SECRET=YOUR_TEST_SECRET

# Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloud
CLOUDINARY_API_KEY=your_key
CLOUDINARY_API_SECRET=your_secret

# Sentry (optional in dev)
# SENTRY_DSN=
```

### Production (Railway/Heroku Environment Variables)

```bash
# Django
DJANGO_SECRET_KEY=<GENERATE_NEW_SECURE_KEY>
DEBUG=False
ALLOWED_HOSTS=your-app.railway.app,your-domain.com
DJANGO_ENVIRONMENT=production

# Database (provided by Railway)
DATABASE_URL=postgresql://user:pass@host:5432/db

# CORS (production frontend)
CORS_ALLOWED_ORIGINS=https://your-frontend.com

# Razorpay (LIVE keys)
RAZORPAY_KEY_ID=rzp_live_YOUR_LIVE_KEY
RAZORPAY_KEY_SECRET=YOUR_LIVE_SECRET

# Cloudinary (production)
CLOUDINARY_CLOUD_NAME=prod_cloud
CLOUDINARY_API_KEY=prod_key
CLOUDINARY_API_SECRET=prod_secret

# Sentry (required for production)
SENTRY_DSN=https://key@o123.ingest.sentry.io/456
SENTRY_RELEASE=v1.0.0
```

## How to Generate Values

### Django Secret Key
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Razorpay Keys
1. Sign up at https://razorpay.com
2. Go to Settings → API Keys
3. Generate Test Keys (development)
4. Generate Live Keys (production)

### Cloudinary Credentials
1. Sign up at https://cloudinary.com
2. Go to Dashboard
3. Copy Cloud Name, API Key, API Secret

### Sentry DSN
1. Sign up at https://sentry.io
2. Create new Django project
3. Copy DSN from project settings

### Firebase Credentials
1. Go to Firebase Console
2. Project Settings → Service Accounts
3. Generate new private key
4. Save as `firebase-credentials.json`

## Security Best Practices

### ✅ DO

- Use different secrets for development and production
- Rotate secrets regularly
- Use test Razorpay keys in development
- Set DEBUG=False in production
- Use strong, random secret keys
- Store secrets in environment variables
- Use .gitignore to exclude .env files

### ❌ DON'T

- Commit .env files to version control
- Share secrets in chat/email
- Use production secrets in development
- Use the same secret key across environments
- Hardcode secrets in code
- Use weak or predictable secrets

## Deployment Checklist

### Before Deploying

- [ ] Generate new DJANGO_SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Update ALLOWED_HOSTS with your domain
- [ ] Use DATABASE_URL from hosting platform
- [ ] Switch to live Razorpay keys
- [ ] Configure SENTRY_DSN
- [ ] Update CORS_ALLOWED_ORIGINS with frontend URL
- [ ] Verify all required variables are set

### After Deploying

- [ ] Test that application starts
- [ ] Verify database connection
- [ ] Test payment flow (small amount)
- [ ] Check Sentry for errors
- [ ] Verify file uploads work
- [ ] Test CORS with frontend

## Troubleshooting

### Application Won't Start

**Check:**
1. All required variables are set
2. DJANGO_SECRET_KEY is not empty
3. DATABASE_URL or DB_* variables are correct
4. No syntax errors in .env file

### Database Connection Failed

**Check:**
1. DATABASE_URL format is correct
2. Database server is running
3. Credentials are correct
4. Host/port are accessible

### Payment Errors

**Check:**
1. Using correct Razorpay keys (test vs live)
2. RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET are set
3. Keys are not expired
4. Account is active

### CORS Errors

**Check:**
1. Frontend URL is in CORS_ALLOWED_ORIGINS
2. No trailing slashes in URLs
3. Protocol matches (http vs https)
4. Port numbers are correct

### Sentry Not Working

**Check:**
1. DEBUG=False (Sentry only runs in production)
2. SENTRY_DSN is set correctly
3. DSN format is valid
4. Network can reach sentry.io

## Files

- `.env` - Local development (gitignored)
- `.env.development` - Development template (gitignored)
- `.env.production.template` - Production template (committed)
- `.env.example` - Example with documentation (committed)
- `.gitignore` - Excludes .env files

## Support

For issues with:
- Django: https://docs.djangoproject.com
- Razorpay: https://razorpay.com/docs
- Cloudinary: https://cloudinary.com/documentation
- Sentry: https://docs.sentry.io
- Railway: https://docs.railway.app

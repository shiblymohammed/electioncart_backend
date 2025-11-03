# Railway Deployment Guide 🚂

Complete guide to deploying the Election Cart backend to Railway.

## Prerequisites

✅ All tasks 1-11 completed  
✅ Code committed to Git repository  
✅ Railway account (free tier available)  
✅ Environment variables documented  

## Quick Start

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Initialize project
cd backend
railway init

# 4. Add PostgreSQL
railway add --plugin postgresql

# 5. Set environment variables
railway variables set DJANGO_SECRET_KEY="your-new-secret-key"
railway variables set DEBUG=False
# ... (see full list below)

# 6. Deploy
railway up
```

## Detailed Steps

### Step 1: Create Railway Account

1. Visit https://railway.app
2. Sign up with GitHub (recommended)
3. Verify email
4. Free tier includes:
   - $5 credit/month
   - 500 hours execution
   - 1GB RAM
   - 1GB storage

### Step 2: Create New Project

**Option A: Via Dashboard (Recommended)**
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Connect your GitHub account
4. Select your repository
5. Select `backend` as root directory

**Option B: Via CLI**
```bash
cd backend
railway init
# Follow prompts to create project
```

### Step 3: Add PostgreSQL Database

**Via Dashboard:**
1. Click "New" → "Database" → "Add PostgreSQL"
2. Railway automatically sets `DATABASE_URL`

**Via CLI:**
```bash
railway add --plugin postgresql
```

### Step 4: Configure Environment Variables

**Required Variables:**

```bash
# Django Core
railway variables set DJANGO_SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
railway variables set DEBUG=False
railway variables set DJANGO_ENVIRONMENT=production

# ALLOWED_HOSTS will be set automatically by Railway
# Or set manually: railway variables set ALLOWED_HOSTS="your-app.railway.app"

# Razorpay (LIVE keys for production)
railway variables set RAZORPAY_KEY_ID="rzp_live_YOUR_KEY"
railway variables set RAZORPAY_KEY_SECRET="YOUR_SECRET"

# Cloudinary
railway variables set CLOUDINARY_CLOUD_NAME="your_cloud"
railway variables set CLOUDINARY_API_KEY="your_key"
railway variables set CLOUDINARY_API_SECRET="your_secret"

# Sentry (get from sentry.io)
railway variables set SENTRY_DSN="https://your-key@o123.ingest.sentry.io/456"

# CORS (your frontend URL)
railway variables set CORS_ALLOWED_ORIGINS="https://your-frontend.com"

# Firebase (if using)
railway variables set FIREBASE_CREDENTIALS_PATH="firebase-credentials.json"
```

**Via Dashboard:**
1. Go to project → Variables
2. Click "New Variable"
3. Add each variable

### Step 5: Deploy

**Via CLI:**
```bash
railway up
```

**Via Dashboard:**
- Push to GitHub
- Railway auto-deploys on push

### Step 6: Monitor Deployment

```bash
# Watch logs
railway logs

# Check status
railway status

# Get URL
railway domain
```

### Step 7: Run Post-Deployment Tasks

```bash
# Create superuser
railway run python manage.py createsuperuser

# Check deployment
railway run python manage.py check --deploy
```

## Environment Variables Reference

### Complete List

```bash
# Django
DJANGO_SECRET_KEY=<generate-new-key>
DEBUG=False
ALLOWED_HOSTS=<auto-set-by-railway>
DJANGO_ENVIRONMENT=production

# Database (auto-set by Railway)
DATABASE_URL=postgresql://...

# Razorpay
RAZORPAY_KEY_ID=rzp_live_...
RAZORPAY_KEY_SECRET=...

# Cloudinary
CLOUDINARY_CLOUD_NAME=...
CLOUDINARY_API_KEY=...
CLOUDINARY_API_SECRET=...

# Sentry
SENTRY_DSN=https://...
SENTRY_RELEASE=v1.0.0  # optional

# CORS
CORS_ALLOWED_ORIGINS=https://your-frontend.com

# Firebase (optional)
FIREBASE_CREDENTIALS_PATH=firebase-credentials.json
```

## Deployment Configuration

Railway uses these files:
- `Procfile` - Defines web process
- `railway.json` - Railway-specific config
- `runtime.txt` - Python version
- `requirements.txt` - Dependencies

All are already configured!

## Custom Domain (Optional)

### Add Custom Domain

1. Go to project → Settings → Domains
2. Click "Add Domain"
3. Enter your domain: `api.yourdomain.com`
4. Add CNAME record to your DNS:
   ```
   CNAME api your-app.railway.app
   ```
5. Wait for SSL certificate (automatic)

### Update ALLOWED_HOSTS

```bash
railway variables set ALLOWED_HOSTS="api.yourdomain.com,your-app.railway.app"
```

### Update CORS

```bash
railway variables set CORS_ALLOWED_ORIGINS="https://yourdomain.com,https://www.yourdomain.com"
```

## Monitoring

### View Logs

```bash
# Real-time logs
railway logs

# Last 100 lines
railway logs --lines 100
```

### Metrics

Dashboard shows:
- CPU usage
- Memory usage
- Network traffic
- Request count

### Health Check

Railway automatically monitors `/health/` endpoint

## Troubleshooting

### Deployment Failed

**Check logs:**
```bash
railway logs
```

**Common issues:**
- Missing environment variables
- Database connection failed
- Static files not collected
- Requirements.txt errors

### Application Won't Start

**Check:**
1. All environment variables set
2. DATABASE_URL is set
3. Procfile is correct
4. Python version matches runtime.txt

**Test locally:**
```bash
# Set environment variables
export DEBUG=False
export DATABASE_URL="postgresql://..."

# Run migrations
python manage.py migrate

# Collect static
python manage.py collectstatic --noinput

# Test gunicorn
gunicorn election_cart.wsgi:application
```

### Database Connection Error

**Check:**
```bash
railway variables
# Verify DATABASE_URL is set

railway run python manage.py dbshell
# Test database connection
```

### Static Files Not Loading

**Check:**
1. `collectstatic` runs in Procfile
2. WhiteNoise middleware configured
3. STATIC_ROOT set correctly

**Force collect:**
```bash
railway run python manage.py collectstatic --noinput --clear
```

### 502 Bad Gateway

**Possible causes:**
- Application crashed
- Gunicorn not starting
- Port binding issue

**Check:**
```bash
railway logs
# Look for startup errors
```

## Cost Management

### Free Tier

- $5 credit/month
- ~500 hours execution
- Sufficient for:
  - Development
  - Small apps
  - Testing

### Usage Monitoring

```bash
railway usage
```

### Optimization Tips

1. **Reduce dyno hours:**
   - Use sleep mode for dev
   - Scale down when not needed

2. **Reduce memory:**
   - Optimize queries
   - Use connection pooling
   - Monitor with `railway metrics`

3. **Reduce bandwidth:**
   - Use Cloudinary for media
   - Enable compression
   - Cache static files

## Scaling

### Vertical Scaling

Upgrade plan for more resources:
- Hobby: $5/month
- Pro: $20/month

### Horizontal Scaling

Add more instances (Pro plan):
```bash
railway scale --replicas 2
```

## Backup and Recovery

### Database Backups

Railway automatically backs up PostgreSQL:
- Daily backups
- 7-day retention (free tier)
- 30-day retention (paid)

### Manual Backup

```bash
# Export database
railway run pg_dump > backup.sql

# Import database
railway run psql < backup.sql
```

### Rollback Deployment

```bash
# View deployments
railway deployments

# Rollback to previous
railway rollback
```

## CI/CD Integration

### GitHub Actions

Railway auto-deploys on push to main branch.

**Custom workflow:**
```yaml
# .github/workflows/deploy.yml
name: Deploy to Railway

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Railway
        run: |
          npm install -g @railway/cli
          railway up
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
```

## Security Checklist

Before going live:

- [ ] New DJANGO_SECRET_KEY generated
- [ ] DEBUG=False
- [ ] Live Razorpay keys configured
- [ ] ALLOWED_HOSTS set correctly
- [ ] CORS_ALLOWED_ORIGINS set
- [ ] SENTRY_DSN configured
- [ ] SSL certificate active
- [ ] Database backups enabled
- [ ] Environment variables secured

## Post-Deployment

### Test Everything

1. **Health Check:**
   ```bash
   curl https://your-app.railway.app/health/
   ```

2. **Admin Panel:**
   ```
   https://your-app.railway.app/admin/
   ```

3. **API Endpoints:**
   ```bash
   curl https://your-app.railway.app/api/packages/
   ```

4. **Payment Flow:**
   - Test with small amount
   - Verify Razorpay integration

5. **File Upload:**
   - Test image upload
   - Verify Cloudinary storage

### Set Up Monitoring

1. **UptimeRobot:**
   - Add monitor for `/health/`
   - Configure email alerts

2. **Sentry:**
   - Verify errors are captured
   - Set up alert rules

3. **Railway Metrics:**
   - Monitor CPU/memory
   - Set up usage alerts

## Support

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Railway Status: https://status.railway.app

## Quick Reference

```bash
# Common Commands
railway login              # Login to Railway
railway init              # Initialize project
railway up                # Deploy
railway logs              # View logs
railway variables         # List variables
railway variables set     # Set variable
railway run <command>     # Run command
railway domain            # Get domain
railway status            # Check status
railway rollback          # Rollback deployment
```

---

**Your app is ready for Railway deployment!** 🚀

All configuration files are in place. Just follow the steps above to deploy.

**Estimated deployment time:** 10-15 minutes  
**Cost:** Free tier ($5 credit/month)

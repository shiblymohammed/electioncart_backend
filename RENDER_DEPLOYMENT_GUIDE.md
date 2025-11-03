# Render.com Deployment Guide 🚀

Complete guide to deploying the Election Cart backend to Render.com (Free Tier).

## Why Render?

- ✅ **Free web service** (with limitations)
- ✅ **Free PostgreSQL** for 90 days, then $7/month
- ✅ Automatic HTTPS/SSL
- ✅ GitHub auto-deploy
- ✅ Easy environment variable management
- ✅ Better free tier than Railway

## Prerequisites

✅ GitHub repository: https://github.com/shiblymohammed/electioncart_backend  
✅ Render account (free): https://render.com  
✅ Environment variables ready  

## Step-by-Step Deployment

### Step 1: Create Render Account

1. Go to https://render.com
2. Sign up with GitHub (recommended)
3. Verify your email

### Step 2: Create PostgreSQL Database

1. From Render Dashboard, click **"New +"**
2. Select **"PostgreSQL"**
3. Configure:
   - **Name**: `electioncart-db`
   - **Database**: `electioncart`
   - **User**: `electioncart_user`
   - **Region**: Choose closest to you
   - **Plan**: **Free** (90 days free, then $7/month)
4. Click **"Create Database"**
5. **Copy the Internal Database URL** (starts with `postgresql://`)

### Step 3: Create Web Service

1. From Render Dashboard, click **"New +"**
2. Select **"Web Service"**
3. Connect your GitHub repository:
   - Click **"Connect account"** if needed
   - Select **"shiblymohammed/electioncart_backend"**
4. Configure the service:

```
Name: electioncart-backend
Region: [Choose closest to you]
Branch: main
Root Directory: [leave empty]
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn election_cart.wsgi:application --bind 0.0.0.0:$PORT
Plan: Free
```

5. Click **"Advanced"** to add environment variables

### Step 4: Configure Environment Variables

Click **"Add Environment Variable"** for each:

```bash
# Django Core
DJANGO_SECRET_KEY=my$m9$s5ell%1#t^3e217%s%fb(ucpme4nql)7c=nl2!$og!!h
DEBUG=False
DJANGO_ENVIRONMENT=production
PYTHON_VERSION=3.11.9

# Database (paste the Internal Database URL from Step 2)
DATABASE_URL=postgresql://electioncart_user:password@hostname/electioncart

# Razorpay (LIVE keys)
RAZORPAY_KEY_ID=rzp_live_RWGCaTq8yBUu1O
RAZORPAY_KEY_SECRET=BkMbLO9W10fvGEwjw4624uY7

# Cloudinary
CLOUDINARY_CLOUD_NAME=dmbrf5xqf
CLOUDINARY_API_KEY=847545154475654
CLOUDINARY_API_SECRET=s6HU7XHz5vqF2bmtKA9cLVuQdvs

# Sentry
SENTRY_DSN=https://c53e3b0f954bb47c1b8e2683a9a324d8@o4510300508782597.ingest.us.sentry.io/4510300511600640

# CORS (update after getting your Render URL)
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### Step 5: Add Build Script

Render needs a build script. Create `build.sh` in your backend folder:

```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
```

Make it executable and commit:
```bash
chmod +x build.sh
git add build.sh
git commit -m "Add Render build script"
git push
```

### Step 6: Update Build Command

Go back to Render dashboard → Your service → Settings:
- **Build Command**: `./build.sh`
- Click **"Save Changes"**

### Step 7: Deploy

1. Click **"Manual Deploy"** → **"Deploy latest commit"**
2. Watch the logs for any errors
3. Wait for deployment to complete (5-10 minutes)

### Step 8: Get Your URL

Once deployed, Render provides a URL like:
```
https://electioncart-backend.onrender.com
```

### Step 9: Update CORS and ALLOWED_HOSTS

1. Go to your service → **Environment**
2. Update:
```bash
CORS_ALLOWED_ORIGINS=https://your-frontend-url.com
```

Render automatically sets `ALLOWED_HOSTS` based on your service URL.

### Step 10: Create Superuser

From Render Dashboard → Your service → **Shell** tab:
```bash
python manage.py createsuperuser
```

Or use Render CLI:
```bash
# Install Render CLI
npm install -g @render/cli

# Login
render login

# Run command
render run python manage.py createsuperuser
```

## Testing Your Deployment

### 1. Health Check
```bash
curl https://electioncart-backend.onrender.com/health/
```

Should return:
```json
{
  "status": "healthy",
  "service": "election-cart-api",
  "database": "connected",
  "timestamp": "2025-11-03T..."
}
```

### 2. Admin Panel
Visit: `https://electioncart-backend.onrender.com/admin/`

### 3. API Endpoints
```bash
curl https://electioncart-backend.onrender.com/api/packages/
```

## Free Tier Limitations

### What's Included (Free):
- ✅ Web service with 750 hours/month
- ✅ Automatic HTTPS
- ✅ GitHub auto-deploy
- ✅ Custom domains
- ✅ Environment variables

### Limitations:
- ⚠️ Service spins down after 15 minutes of inactivity
- ⚠️ First request after spin-down takes 30-60 seconds
- ⚠️ 512 MB RAM
- ⚠️ Shared CPU

### PostgreSQL Free Tier:
- ✅ Free for 90 days
- ⚠️ Then $7/month
- ✅ 1 GB storage
- ✅ Daily backups

## Upgrading (Optional)

If you need better performance:

### Starter Plan ($7/month):
- No spin-down
- 512 MB RAM
- Faster response times

### Standard Plan ($25/month):
- 2 GB RAM
- Better performance
- Priority support

## Monitoring

### View Logs
Render Dashboard → Your service → **Logs** tab

### Metrics
Render Dashboard → Your service → **Metrics** tab shows:
- CPU usage
- Memory usage
- Request count
- Response times

### Alerts
Set up email alerts:
1. Go to service → **Settings**
2. Scroll to **Notifications**
3. Add email for deployment failures

## Troubleshooting

### Deployment Failed

**Check logs:**
Render Dashboard → Your service → **Logs**

**Common issues:**
- Missing environment variables
- Database connection failed
- Build script errors
- Requirements.txt issues

### Service Won't Start

**Check:**
1. All environment variables set correctly
2. DATABASE_URL is correct (use Internal URL)
3. Build script ran successfully
4. Python version matches runtime.txt

### Database Connection Error

**Verify:**
1. DATABASE_URL uses **Internal Database URL** (not External)
2. Database is running (check database dashboard)
3. SSL is configured correctly

### Static Files Not Loading

**Check:**
1. `collectstatic` runs in build.sh
2. WhiteNoise is in MIDDLEWARE
3. STATIC_ROOT is set correctly

### Slow First Request

This is normal on free tier - service spins down after 15 minutes of inactivity.

**Solutions:**
1. Upgrade to Starter plan ($7/month) - no spin-down
2. Use a cron job to ping your service every 10 minutes
3. Accept the limitation for development/testing

## Auto-Deploy from GitHub

Render automatically deploys when you push to GitHub!

```bash
# Make changes
git add .
git commit -m "Update feature"
git push

# Render automatically deploys
```

## Custom Domain (Optional)

### Add Custom Domain

1. Go to service → **Settings** → **Custom Domains**
2. Click **"Add Custom Domain"**
3. Enter your domain: `api.yourdomain.com`
4. Add CNAME record to your DNS:
   ```
   CNAME api electioncart-backend.onrender.com
   ```
5. Wait for SSL certificate (automatic)

## Cost Comparison

| Service | Free Tier | Paid Tier |
|---------|-----------|-----------|
| **Render** | Free web service + 90 days DB | $7/month (Starter) |
| **Railway** | $5 credit/month | $20/month (Hobby) |
| **Heroku** | No free tier | $7/month (Eco) |
| **DigitalOcean** | No free tier | $12/month (Basic) |

**Recommendation**: Start with Render free tier, upgrade database to $7/month after 90 days.

## Backup Strategy

### Database Backups

Render automatically backs up PostgreSQL:
- Daily backups (free tier)
- 7-day retention
- One-click restore

### Manual Backup

```bash
# Export database
render pg:dump electioncart-db > backup.sql

# Import database
render pg:restore electioncart-db < backup.sql
```

## Support

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com
- **Render Status**: https://status.render.com

## Quick Reference

```bash
# Install Render CLI
npm install -g @render/cli

# Login
render login

# List services
render services list

# View logs
render logs electioncart-backend

# Run command
render run python manage.py createsuperuser

# Open shell
render shell electioncart-backend
```

---

**Your backend is ready for Render deployment!** 🚀

**Estimated deployment time**: 10-15 minutes  
**Cost**: Free (90 days), then $7/month for database

**Next Steps**:
1. Create Render account
2. Create PostgreSQL database
3. Create web service
4. Configure environment variables
5. Deploy!

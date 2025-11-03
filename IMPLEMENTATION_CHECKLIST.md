# ✅ Implementation Checklist - Small Scale Production

**Use this checklist to track your progress**  
**Estimated Time: 2-3 days (10-12 hours total)**

---

## Day 1: Security & Configuration (6 hours)

### Morning Session (3 hours)

#### ☐ 1. Rotate Secrets (30 min)
```bash
# Generate new SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
- [ ] Copy new SECRET_KEY
- [ ] Update .env.production (don't commit!)
- [ ] Use Razorpay TEST keys for staging
- [ ] Change database password
- [ ] Verify .env is in .gitignore

#### ☐ 2. Fix DEBUG Mode (15 min)
**File: `backend/election_cart/settings.py`**
- [ ] Change line 17: `DEBUG = os.getenv('DEBUG', 'False') == 'True'`
- [ ] Test locally with DEBUG=False
- [ ] Create templates/404.html
- [ ] Create templates/500.html

#### ☐ 3. Add Security Headers (30 min)
**File: `backend/election_cart/settings.py`**
- [ ] Add security settings block (see plan)
- [ ] Test with DEBUG=False locally
- [ ] Verify no errors

#### ☐ 4. Add Logging (45 min)
**File: `backend/election_cart/settings.py`**
- [ ] Add LOGGING configuration
- [ ] Create logs/ directory
- [ ] Add logs/ to .gitignore
- [ ] Test logging works: `python manage.py check`
- [ ] Check logs/django.log file created

#### ☐ 5. Add Health Check (30 min)
**File: `backend/election_cart/urls.py`**
- [ ] Add health_check function
- [ ] Add path('health/', health_check)
- [ ] Test: http://localhost:8000/health/
- [ ] Should return {"status": "healthy"}

#### ☐ 6. Coffee Break ☕ (15 min)

---

### Afternoon Session (3 hours)

#### ☐ 7. Install Rate Limiting (1 hour)
```bash
pip install django-ratelimit
```

**File: `backend/authentication/views.py`**
- [ ] Import ratelimit decorator
- [ ] Add @ratelimit to login view
- [ ] Add @ratelimit to signup view
- [ ] Add rate limit check in each view

**File: `backend/orders/views.py`**
- [ ] Add @ratelimit to create_order view
- [ ] Add rate limit check

**Test:**
- [ ] Try 6 rapid login attempts
- [ ] Should get 429 error on 6th attempt

#### ☐ 8. Install Production Dependencies (30 min)
```bash
pip install whitenoise dj-database-url sentry-sdk gunicorn
pip freeze > requirements.txt
```
- [ ] Verify requirements.txt updated
- [ ] Commit requirements.txt

#### ☐ 9. Configure WhiteNoise (30 min)
**File: `backend/election_cart/settings.py`**
- [ ] Add WhiteNoise to MIDDLEWARE
- [ ] Add STATICFILES_STORAGE setting
- [ ] Run: `python manage.py collectstatic`
- [ ] Verify staticfiles/ directory created

#### ☐ 10. Run Security Check (30 min)
```bash
python manage.py check --deploy
```
- [ ] Fix any warnings
- [ ] Document any warnings you can't fix
- [ ] Re-run until clean

---

## Day 2: Infrastructure & Deployment (4-5 hours)

### Morning Session (2-3 hours)

#### ☐ 11. Sign Up for Services (30 min)
- [ ] Railway account (https://railway.app)
- [ ] Sentry account (https://sentry.io)
- [ ] UptimeRobot account (https://uptimerobot.com)

#### ☐ 12. Set Up Railway Project (1 hour)
```bash
npm install -g @railway/cli
railway login
cd backend
railway init
```
- [ ] Create new project
- [ ] Add PostgreSQL plugin
- [ ] Copy DATABASE_URL from Railway dashboard

#### ☐ 13. Configure Database (30 min)
**File: `backend/election_cart/settings.py`**
- [ ] Add dj_database_url configuration
- [ ] Test locally with DATABASE_URL
- [ ] Verify connection works

#### ☐ 14. Configure Sentry (30 min)
- [ ] Create Sentry project
- [ ] Copy DSN
- [ ] Add Sentry configuration to settings.py
- [ ] Test error tracking (trigger an error)
- [ ] Check Sentry dashboard for error

---

### Afternoon Session (2 hours)

#### ☐ 15. Set Environment Variables in Railway (30 min)
In Railway dashboard, add:
- [ ] DJANGO_SECRET_KEY=<new-key>
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS=<your-app>.railway.app
- [ ] RAZORPAY_KEY_ID=<your-key>
- [ ] RAZORPAY_KEY_SECRET=<your-secret>
- [ ] CLOUDINARY_CLOUD_NAME=<your-cloud>
- [ ] CLOUDINARY_API_KEY=<your-key>
- [ ] CLOUDINARY_API_SECRET=<your-secret>
- [ ] SENTRY_DSN=<your-dsn>
- [ ] CORS_ALLOWED_ORIGINS=https://<your-frontend>.com

#### ☐ 16. Create Procfile (15 min)
**File: `backend/Procfile`**
```
web: python manage.py migrate && gunicorn election_cart.wsgi:application --bind 0.0.0.0:$PORT
```
- [ ] Create Procfile
- [ ] Commit and push

#### ☐ 17. Deploy to Railway (30 min)
```bash
railway up
```
- [ ] Wait for deployment
- [ ] Check logs for errors
- [ ] Get domain: `railway domain`

#### ☐ 18. Test Deployment (45 min)
- [ ] Visit https://<your-app>.railway.app/health/
- [ ] Should return {"status": "healthy"}
- [ ] Visit https://<your-app>.railway.app/admin/
- [ ] Create superuser: `railway run python manage.py createsuperuser`
- [ ] Login to admin panel
- [ ] Test API endpoints
- [ ] Test file upload
- [ ] Test payment flow (test mode)

---

## Day 3: Monitoring & Final Testing (2-3 hours)

### Morning Session (1-2 hours)

#### ☐ 19. Set Up UptimeRobot (15 min)
- [ ] Add monitor for health endpoint
- [ ] Set check interval: 5 minutes
- [ ] Add email alert
- [ ] Test alert (pause monitor, wait for email)

#### ☐ 20. Security Testing (30 min)
- [ ] Visit https://securityheaders.com
- [ ] Enter your domain
- [ ] Should get A or A+ rating
- [ ] Fix any issues

- [ ] Test HTTPS redirect
- [ ] Visit http://<your-app>.railway.app
- [ ] Should redirect to https://

- [ ] Test rate limiting
- [ ] Try 6 rapid login attempts
- [ ] Should get rate limited

#### ☐ 21. Functionality Testing (45 min)
**Authentication:**
- [ ] Signup new user
- [ ] Login
- [ ] Logout
- [ ] Login again

**Products:**
- [ ] View packages
- [ ] View campaigns
- [ ] View product details

**Cart:**
- [ ] Add package to cart
- [ ] Add campaign to cart
- [ ] View cart
- [ ] Update quantities
- [ ] Remove items

**Orders:**
- [ ] Create order
- [ ] Payment flow (test mode)
- [ ] Upload resources
- [ ] View order details

**Admin:**
- [ ] Login to admin panel
- [ ] View orders
- [ ] Assign order to staff
- [ ] Update checklist

---

### Afternoon Session (1 hour)

#### ☐ 22. Performance Testing (30 min)
- [ ] Test API response times (should be < 500ms)
- [ ] Test file upload (should work for 5MB files)
- [ ] Test image loading from Cloudinary
- [ ] Test with slow 3G connection

#### ☐ 23. Error Testing (30 min)
- [ ] Trigger 404 error (visit /nonexistent)
- [ ] Should show custom 404 page
- [ ] Check Sentry for error

- [ ] Trigger 500 error (create one in code temporarily)
- [ ] Should show custom 500 page
- [ ] Check Sentry for error
- [ ] Fix the error

#### ☐ 24. Final Checks (30 min)
- [ ] Check logs in Railway dashboard
- [ ] Check database has data
- [ ] Check Cloudinary has uploaded images
- [ ] Check Sentry dashboard
- [ ] Check UptimeRobot status

---

## 🎉 Go Live Checklist

### Pre-Launch
- [ ] All tests passing
- [ ] No errors in logs
- [ ] Sentry configured and working
- [ ] UptimeRobot monitoring active
- [ ] Database backups enabled
- [ ] Custom domain configured (optional)
- [ ] SSL certificate active
- [ ] CORS configured for frontend domain

### Launch
- [ ] Update frontend API URL
- [ ] Deploy frontend
- [ ] Test end-to-end flow
- [ ] Monitor logs for 1 hour
- [ ] Check Sentry for errors

### Post-Launch (First 24 Hours)
- [ ] Monitor error logs
- [ ] Check Sentry dashboard
- [ ] Verify backups running
- [ ] Test from different devices
- [ ] Check response times
- [ ] Monitor database connections

### Post-Launch (First Week)
- [ ] Review all error logs
- [ ] Analyze performance metrics
- [ ] Check for slow queries
- [ ] Review security logs
- [ ] Test backup restoration
- [ ] Verify monitoring alerts work

---

## 📊 Progress Tracker

**Day 1:** ☐ Security & Configuration (6 hours)
- Morning: ☐☐☐☐☐☐ (6 tasks)
- Afternoon: ☐☐☐☐ (4 tasks)

**Day 2:** ☐ Infrastructure & Deployment (4-5 hours)
- Morning: ☐☐☐☐ (4 tasks)
- Afternoon: ☐☐☐☐ (4 tasks)

**Day 3:** ☐ Monitoring & Testing (2-3 hours)
- Morning: ☐☐☐ (3 tasks)
- Afternoon: ☐☐☐ (3 tasks)

**Total:** 0/24 tasks completed

---

## 🆘 Troubleshooting

### If deployment fails:
1. Check Railway logs
2. Check for missing environment variables
3. Check database connection
4. Check Procfile syntax

### If health check fails:
1. Check database connection
2. Check logs for errors
3. Verify migrations ran
4. Check ALLOWED_HOSTS

### If static files don't load:
1. Run collectstatic again
2. Check WhiteNoise configuration
3. Check STATIC_ROOT setting
4. Clear browser cache

### If rate limiting doesn't work:
1. Check decorator syntax
2. Check if limited attribute exists
3. Test with different IPs
4. Check logs for errors

---

## 📞 Need Help?

- **Railway Docs:** https://docs.railway.app
- **Django Docs:** https://docs.djangoproject.com
- **Sentry Docs:** https://docs.sentry.io
- **WhiteNoise Docs:** http://whitenoise.evans.io

---

**Good luck! You've got this! 🚀**

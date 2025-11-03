# Render Environment Variables Setup Guide 🔧

## Quick Copy-Paste Method

Render allows you to bulk import environment variables from a `.env` file format!

### Step 1: Copy the Environment Variables

Open the file `.env.render` in your backend folder and **copy everything**.

Or copy this:

```env
DJANGO_SECRET_KEY=my$m9$s5ell%1#t^3e217%s%fb(ucpme4nql)7c=nl2!$og!!h
DEBUG=False
DJANGO_ENVIRONMENT=production
PYTHON_VERSION=3.11.9
RAZORPAY_KEY_ID=rzp_live_RWGCaTq8yBUu1O
RAZORPAY_KEY_SECRET=BkMbLO9W10fvGEwjw4624uY7
CLOUDINARY_CLOUD_NAME=dmbrf5xqf
CLOUDINARY_API_KEY=847545154475654
CLOUDINARY_API_SECRET=s6HU7XHz5vqF2bmtKA9cLVuQdvs
SENTRY_DSN=https://c53e3b0f954bb47c1b8e2683a9a324d8@o4510300508782597.ingest.us.sentry.io/4510300511600640
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Step 2: Paste into Render

1. In Render dashboard, go to your web service
2. Click **"Environment"** tab on the left
3. Click **"Add from .env"** button
4. **Paste** the entire content from above
5. Click **"Save Changes"**

That's it! All variables will be imported at once. ✅

---

## Alternative: Manual Entry

If you prefer to add them one by one:

### Required Variables:

| Key | Value |
|-----|-------|
| `DJANGO_SECRET_KEY` | `my$m9$s5ell%1#t^3e217%s%fb(ucpme4nql)7c=nl2!$og!!h` |
| `DEBUG` | `False` |
| `DJANGO_ENVIRONMENT` | `production` |
| `PYTHON_VERSION` | `3.11.9` |
| `RAZORPAY_KEY_ID` | `rzp_live_RWGCaTq8yBUu1O` |
| `RAZORPAY_KEY_SECRET` | `BkMbLO9W10fvGEwjw4624uY7` |
| `CLOUDINARY_CLOUD_NAME` | `dmbrf5xqf` |
| `CLOUDINARY_API_KEY` | `847545154475654` |
| `CLOUDINARY_API_SECRET` | `s6HU7XHz5vqF2bmtKA9cLVuQdvs` |
| `SENTRY_DSN` | `https://c53e3b0f954bb47c1b8e2683a9a324d8@o4510300508782597.ingest.us.sentry.io/4510300511600640` |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:3000,http://localhost:5173` |

---

## Important Notes

### ✅ DO NOT SET These (Render sets automatically):
- `DATABASE_URL` - Automatically set when you add PostgreSQL
- `ALLOWED_HOSTS` - Automatically set based on your Render domain
- `PORT` - Automatically set by Render

### ⚠️ Update After Deployment:
Once your frontend is deployed, update:
```
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### 🔐 Security:
- The `.env.render` file is in `.gitignore` and will NOT be committed to Git
- These are your LIVE production credentials
- Keep them secure!

---

## Verification Checklist

After adding environment variables, verify:

- ✅ `DJANGO_SECRET_KEY` is set (different from development)
- ✅ `DEBUG` is set to `False`
- ✅ `RAZORPAY_KEY_ID` starts with `rzp_live_` (not `rzp_test_`)
- ✅ All Cloudinary variables are set
- ✅ `SENTRY_DSN` is set
- ✅ `PYTHON_VERSION` is `3.11.9`

---

## Troubleshooting

### If deployment fails with "Missing environment variable":
1. Check that all variables from the list above are set
2. Make sure there are no typos in variable names
3. Verify no extra spaces in values

### If database connection fails:
1. Make sure you created a PostgreSQL database in Render
2. Verify `DATABASE_URL` is automatically set (don't set it manually)
3. Check that the database and web service are in the same region

### If static files don't load:
1. Verify `PYTHON_VERSION=3.11.9` is set
2. Check that `build.sh` ran successfully in deployment logs
3. Verify WhiteNoise is in MIDDLEWARE (it is in our settings.py)

---

## Quick Reference

### To view all environment variables:
Render Dashboard → Your Service → Environment tab

### To update a variable:
1. Click on the variable
2. Edit the value
3. Click "Save Changes"
4. Service will automatically redeploy

### To delete a variable:
1. Click the trash icon next to the variable
2. Confirm deletion
3. Click "Save Changes"

---

**Ready to deploy!** 🚀

Copy the variables from `.env.render` and paste them into Render using the "Add from .env" feature.

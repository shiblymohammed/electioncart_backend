# Admin Frontend Login Issue - CORS Fix

## Problem
The admin frontend can't login, but Django admin panel works fine.

## Root Cause
The backend's CORS configuration doesn't include the admin frontend URL.

## Solution

### Step 1: Find Your Admin Frontend URL
After deploying to Vercel/Netlify, you'll get a URL like:
- `https://electioncart-admin.vercel.app`
- `https://electioncart-admin.netlify.app`

### Step 2: Update Backend CORS Settings on Render

1. Go to Render Dashboard
2. Select your backend service
3. Go to **Environment** tab
4. Add or update the `CORS_ALLOWED_ORIGINS` variable:

```
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000,http://localhost:5174,https://your-admin-frontend-url.vercel.app,https://your-customer-frontend-url.vercel.app
```

**Example:**
```
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000,http://localhost:5174,https://electioncart-admin.vercel.app,https://electioncart-frontend.vercel.app
```

### Step 3: Redeploy Backend
After updating the environment variable, Render will automatically redeploy.

### Step 4: Test Login
Try logging in to the admin frontend again with:
- Username: `aseeb`
- Password: `Dr.aseeb123`

## Temporary Testing Solution (NOT for production)

If you want to test quickly, you can temporarily allow all origins:

Add this to Render environment:
```
CORS_ALLOW_ALL_ORIGINS=True
```

**⚠️ WARNING:** Remove this after testing! It's a security risk.

## Verify CORS is Working

Open browser console (F12) when trying to login. If you see errors like:
- `Access to XMLHttpRequest blocked by CORS policy`
- `No 'Access-Control-Allow-Origin' header`

Then CORS is definitely the issue.

## Current Backend URL
```
https://electioncart-backend.onrender.com
```

## Login Credentials
- **Username:** aseeb
- **Password:** Dr.aseeb123
- **Role:** admin (set automatically by create_superuser.py)

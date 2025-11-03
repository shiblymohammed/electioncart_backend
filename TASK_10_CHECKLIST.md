# Task 10: Uptime Monitoring Setup Checklist ✅

## Quick Setup Checklist

### Prerequisites
- [ ] Health check endpoint working (`/health/`)
- [ ] Application deployed to production
- [ ] Production URL accessible

### Account Setup
- [ ] Create UptimeRobot account at https://uptimerobot.com
- [ ] Verify email address
- [ ] Log in to dashboard

### Monitor Configuration
- [ ] Click "Add New Monitor"
- [ ] Set Monitor Type: HTTP(s)
- [ ] Set Friendly Name: "Election Cart API - Health Check"
- [ ] Set URL: `https://your-app.railway.app/health/`
- [ ] Set Interval: 5 minutes
- [ ] Set Keyword: "healthy"
- [ ] Set Alert After: 3 consecutive failures
- [ ] Click "Create Monitor"

### Alert Setup
- [ ] Go to "My Settings" → "Alert Contacts"
- [ ] Add email address
- [ ] Verify email
- [ ] Assign to monitor
- [ ] Configure alert preferences

### Testing
- [ ] Wait for first check (5 minutes)
- [ ] Verify status shows "Up"
- [ ] Check response time (should be < 500ms)
- [ ] Optional: Test alert by stopping app

### Documentation
- [ ] Save UptimeRobot dashboard URL
- [ ] Document alert contacts
- [ ] Note monitor settings

## Verification

Monitor should show:
```
Status: ● Up
Uptime: 100%
Response Time: ~50-200ms
Last Check: < 5 minutes ago
```

## Task Complete When:
- ✅ Monitor created and active
- ✅ Status shows "Up"
- ✅ Email alerts configured
- ✅ First successful check completed

---

**Estimated Time**: 10-15 minutes  
**Cost**: Free  
**Next Task**: Task 11 - Create Deployment Configuration Files

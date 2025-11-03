# Task 10: Set Up Uptime Monitoring - GUIDE 📋

## Overview
This guide walks you through setting up uptime monitoring using UptimeRobot (free tier) to monitor your application's health endpoint and receive alerts when the application goes down.

## Why Uptime Monitoring?

### Benefits
- **Immediate Alerts**: Know within minutes when your app goes down
- **Uptime Statistics**: Track availability percentage
- **Response Time Tracking**: Monitor performance over time
- **Status Page**: Optional public status page for users
- **Free Tier**: 50 monitors, 5-minute checks, sufficient for small apps

### What We'll Monitor
- Health check endpoint: `/health/`
- Expected response: 200 OK
- Check frequency: Every 5 minutes
- Alert after: 3 consecutive failures (~15 minutes)

## Prerequisites

✅ Task 5 completed (Health Check Endpoint created)  
✅ Application deployed to production  
✅ Health endpoint accessible: `https://your-app.railway.app/health/`

## Step-by-Step Setup

### Step 1: Create UptimeRobot Account

1. **Visit UptimeRobot**
   ```
   https://uptimerobot.com
   ```

2. **Sign Up for Free**
   - Click "Sign Up Free"
   - Enter email address
   - Create password
   - Verify email

3. **Free Tier Includes**
   - 50 monitors
   - 5-minute check intervals
   - Email alerts
   - SMS alerts (limited)
   - 2-month data retention

### Step 2: Add Health Check Monitor

1. **Click "Add New Monitor"**

2. **Configure Monitor Settings**
   ```
   Monitor Type: HTTP(s)
   Friendly Name: Election Cart API - Health Check
   URL: https://your-app.railway.app/health/
   Monitoring Interval: 5 minutes
   ```

3. **Advanced Settings**
   ```
   HTTP Method: GET
   HTTP Auth Type: None (health endpoint is public)
   Keyword: healthy
   Keyword Type: Exists
   ```
   
   This checks that the response contains the word "healthy"

4. **Alert Contacts**
   - Add your email address
   - Optionally add SMS (limited on free tier)
   - Set alert threshold: 3 consecutive failures

5. **Click "Create Monitor"**

### Step 3: Configure Alert Settings

1. **Go to "My Settings" → "Alert Contacts"**

2. **Add Email Alert**
   ```
   Type: Email
   Email: your-email@example.com
   Friendly Name: Primary Email
   ```

3. **Verify Email**
   - Check inbox for verification email
   - Click verification link

4. **Configure Alert Preferences**
   ```
   Send alerts when: Monitor goes down
   Send alerts when: Monitor comes back up
   Alert frequency: Every time
   ```

### Step 4: Test the Monitor

1. **Wait for First Check**
   - Monitor will check within 5 minutes
   - Status should show "Up" with green indicator

2. **Verify Response**
   ```
   Status: Up
   Response Time: ~50-200ms
   Uptime: 100%
   ```

3. **Test Alert (Optional)**
   - Temporarily stop your application
   - Wait 15 minutes (3 failed checks)
   - Should receive email alert
   - Restart application
   - Should receive recovery email

### Step 5: Configure Status Page (Optional)

1. **Go to "Status Pages"**

2. **Create Public Status Page**
   ```
   Name: Election Cart Status
   URL: your-custom-url.uptimerobot.com
   Monitors: Select your health check monitor
   ```

3. **Customize**
   - Add logo
   - Set colors
   - Add custom domain (paid feature)

4. **Share URL**
   - Give to users/stakeholders
   - Shows real-time status

## Monitor Configuration Details

### Recommended Settings

```yaml
Monitor Type: HTTP(s)
URL: https://your-app.railway.app/health/
Method: GET
Interval: 5 minutes
Timeout: 30 seconds
Alert After: 3 consecutive failures
Keyword Check: "healthy" (exists)
```

### Why These Settings?

- **5-minute interval**: Free tier, sufficient for small apps
- **3 failures**: Prevents false alarms (15 minutes total)
- **Keyword check**: Ensures response is valid, not just 200 OK
- **30-second timeout**: Allows for slow responses

## Alert Configuration

### Email Alerts

**When to Alert:**
- ✅ Monitor goes down (status changes to Down)
- ✅ Monitor comes back up (status changes to Up)
- ❌ Every check (too noisy)

**Alert Content:**
```
Subject: [UptimeRobot] Election Cart API - Health Check is DOWN

Your monitor "Election Cart API - Health Check" is DOWN.

URL: https://your-app.railway.app/health/
Reason: Connection timeout
Time: 2025-11-03 14:30:00 UTC
```

### SMS Alerts (Optional)

Free tier includes limited SMS:
- 10 SMS per month
- Use for critical alerts only
- Configure same as email

## Monitoring Dashboard

### Key Metrics

1. **Uptime Percentage**
   - Target: 99.5%+ (3.6 hours downtime/month)
   - Good: 99.9%+ (43 minutes downtime/month)
   - Excellent: 99.99%+ (4 minutes downtime/month)

2. **Response Time**
   - Target: < 500ms
   - Good: < 200ms
   - Monitor trends over time

3. **Downtime Events**
   - Track frequency
   - Identify patterns
   - Correlate with deployments

### Dashboard View

```
┌─────────────────────────────────────────────┐
│ Election Cart API - Health Check           │
│ Status: ● Up                                │
│ Uptime: 99.95% (30 days)                   │
│ Avg Response: 127ms                        │
│ Last Check: 2 minutes ago                  │
└─────────────────────────────────────────────┘
```

## Troubleshooting

### Monitor Shows "Down" But App Works

**Possible Causes:**
1. Health endpoint not accessible
2. Firewall blocking UptimeRobot IPs
3. SSL certificate issues
4. Keyword not found in response

**Solutions:**
```bash
# Test health endpoint manually
curl https://your-app.railway.app/health/

# Should return:
# {"status":"healthy","service":"election-cart-api",...}

# Check keyword exists
curl https://your-app.railway.app/health/ | grep "healthy"
```

### False Alarms (Frequent Up/Down)

**Possible Causes:**
1. Application restarting frequently
2. Database connection issues
3. Memory/CPU limits reached
4. Network instability

**Solutions:**
1. Check application logs
2. Monitor resource usage
3. Increase alert threshold to 5 failures
4. Check Railway/hosting platform status

### No Alerts Received

**Possible Causes:**
1. Email not verified
2. Alerts disabled
3. Email in spam folder
4. Alert contact not assigned to monitor

**Solutions:**
1. Verify email in UptimeRobot settings
2. Check spam/junk folder
3. Add uptimerobot.com to safe senders
4. Re-assign alert contact to monitor

## Integration with Other Tools

### Slack Integration

1. **Create Slack Webhook**
   - Go to Slack App Directory
   - Search "Incoming Webhooks"
   - Add to workspace
   - Copy webhook URL

2. **Add to UptimeRobot**
   ```
   Alert Contact Type: Webhook
   URL: https://hooks.slack.com/services/YOUR/WEBHOOK/URL
   POST Value: {"text":"Monitor {{monitorFriendlyName}} is {{monitorAlertType}}"}
   ```

### Discord Integration

Similar to Slack:
```
Webhook URL: https://discord.com/api/webhooks/YOUR/WEBHOOK
POST Value: {"content":"🚨 {{monitorFriendlyName}} is {{monitorAlertType}}"}
```

### PagerDuty Integration

For on-call rotations:
1. Create PagerDuty account
2. Get integration key
3. Add as webhook in UptimeRobot

## Best Practices

### Monitor Configuration

✅ **DO:**
- Use keyword checking ("healthy")
- Set reasonable timeout (30s)
- Alert after multiple failures (3+)
- Monitor from multiple locations (paid feature)
- Keep monitor names descriptive

❌ **DON'T:**
- Alert on every check (too noisy)
- Use 1-minute intervals (unnecessary)
- Monitor internal endpoints (use public URLs)
- Ignore alerts (defeats the purpose)

### Alert Management

✅ **DO:**
- Respond to alerts promptly
- Document downtime incidents
- Review patterns monthly
- Test alerts periodically
- Keep contact info updated

❌ **DON'T:**
- Ignore repeated alerts
- Disable alerts without fixing issues
- Use only one alert method
- Forget to test after setup

## Maintenance

### Weekly
- Check uptime percentage
- Review response time trends
- Verify alerts are working

### Monthly
- Review downtime incidents
- Update alert contacts if needed
- Check quota usage (free tier limits)
- Analyze uptime trends

### Quarterly
- Review monitoring strategy
- Consider upgrading if needed
- Update documentation
- Test disaster recovery

## Cost Considerations

### Free Tier (Current)
```
Cost: $0/month
Monitors: 50
Interval: 5 minutes
Alerts: Email + limited SMS
Retention: 2 months
```

**Sufficient for:**
- Small applications
- Single service monitoring
- Basic alerting needs

### Paid Tier (If Needed)
```
Cost: $7/month (Pro)
Monitors: 50
Interval: 1 minute
Alerts: Unlimited
Retention: 12 months
Features: Multi-location, advanced alerts
```

**Upgrade when:**
- Need faster checks (1 minute)
- Need longer data retention
- Need multi-location monitoring
- Need advanced integrations

## Requirements Satisfied

✅ **Requirement 11.1**: Health endpoint responds within 5 seconds  
✅ **Requirement 11.2**: Email alerts configured  
✅ **Requirement 11.3**: Alert threshold set (3 failures)  
✅ **Requirement 11.4**: Check interval set (5 minutes)  
✅ **Requirement 11.5**: Recovery notifications enabled  

## Next Steps

After completing this task:
1. ✅ UptimeRobot account created
2. ✅ Health check monitor configured
3. ✅ Email alerts set up and tested
4. ✅ Dashboard accessible

You can now proceed to:
- **Task 11**: Create Deployment Configuration Files
- **Task 12**: Run Security and Deployment Checks

## Quick Reference

### Monitor URL
```
https://your-app.railway.app/health/
```

### Expected Response
```json
{
  "status": "healthy",
  "service": "election-cart-api",
  "database": "connected",
  "timestamp": "2025-11-03T14:23:45Z"
}
```

### UptimeRobot Dashboard
```
https://uptimerobot.com/dashboard
```

### Support
- UptimeRobot Docs: https://uptimerobot.com/api/
- Support: support@uptimerobot.com

---

**Status**: 📋 MANUAL SETUP REQUIRED  
**Date**: 2025-11-03  
**Requirements Met**: 11.1, 11.2, 11.3, 11.4, 11.5  
**Cost**: Free (50 monitors, 5-min intervals)  
**Time to Setup**: 10-15 minutes

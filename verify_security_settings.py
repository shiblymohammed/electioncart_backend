#!/usr/bin/env python
"""
Verify that all security settings are properly configured in settings.py
"""

import os
import sys

# Set DEBUG to False to test production settings
os.environ['DEBUG'] = 'False'

# Import settings
from election_cart import settings

def verify_settings():
    """Verify all security settings are correctly configured"""
    print("🔒 Verifying Security Settings Configuration\n")
    print("=" * 70)
    
    checks = []
    
    # Check DEBUG mode
    checks.append(("DEBUG Mode", settings.DEBUG == False, f"DEBUG = {settings.DEBUG}"))
    
    # Check HTTPS redirect
    checks.append(("HTTPS Redirect", 
                   hasattr(settings, 'SECURE_SSL_REDIRECT') and settings.SECURE_SSL_REDIRECT == True,
                   f"SECURE_SSL_REDIRECT = {getattr(settings, 'SECURE_SSL_REDIRECT', 'NOT SET')}"))
    
    # Check HSTS
    checks.append(("HSTS Enabled", 
                   hasattr(settings, 'SECURE_HSTS_SECONDS') and settings.SECURE_HSTS_SECONDS == 31536000,
                   f"SECURE_HSTS_SECONDS = {getattr(settings, 'SECURE_HSTS_SECONDS', 'NOT SET')}"))
    
    checks.append(("HSTS Subdomains", 
                   hasattr(settings, 'SECURE_HSTS_INCLUDE_SUBDOMAINS') and settings.SECURE_HSTS_INCLUDE_SUBDOMAINS == True,
                   f"SECURE_HSTS_INCLUDE_SUBDOMAINS = {getattr(settings, 'SECURE_HSTS_INCLUDE_SUBDOMAINS', 'NOT SET')}"))
    
    checks.append(("HSTS Preload", 
                   hasattr(settings, 'SECURE_HSTS_PRELOAD') and settings.SECURE_HSTS_PRELOAD == True,
                   f"SECURE_HSTS_PRELOAD = {getattr(settings, 'SECURE_HSTS_PRELOAD', 'NOT SET')}"))
    
    # Check secure cookies
    checks.append(("Secure Session Cookie", 
                   hasattr(settings, 'SESSION_COOKIE_SECURE') and settings.SESSION_COOKIE_SECURE == True,
                   f"SESSION_COOKIE_SECURE = {getattr(settings, 'SESSION_COOKIE_SECURE', 'NOT SET')}"))
    
    checks.append(("Secure CSRF Cookie", 
                   hasattr(settings, 'CSRF_COOKIE_SECURE') and settings.CSRF_COOKIE_SECURE == True,
                   f"CSRF_COOKIE_SECURE = {getattr(settings, 'CSRF_COOKIE_SECURE', 'NOT SET')}"))
    
    # Check content type options
    checks.append(("Content Type Nosniff", 
                   hasattr(settings, 'SECURE_CONTENT_TYPE_NOSNIFF') and settings.SECURE_CONTENT_TYPE_NOSNIFF == True,
                   f"SECURE_CONTENT_TYPE_NOSNIFF = {getattr(settings, 'SECURE_CONTENT_TYPE_NOSNIFF', 'NOT SET')}"))
    
    # Check XSS filter
    checks.append(("XSS Filter", 
                   hasattr(settings, 'SECURE_BROWSER_XSS_FILTER') and settings.SECURE_BROWSER_XSS_FILTER == True,
                   f"SECURE_BROWSER_XSS_FILTER = {getattr(settings, 'SECURE_BROWSER_XSS_FILTER', 'NOT SET')}"))
    
    # Check X-Frame-Options
    checks.append(("X-Frame-Options", 
                   hasattr(settings, 'X_FRAME_OPTIONS') and settings.X_FRAME_OPTIONS == 'DENY',
                   f"X_FRAME_OPTIONS = {getattr(settings, 'X_FRAME_OPTIONS', 'NOT SET')}"))
    
    # Check proxy headers
    checks.append(("Proxy SSL Header", 
                   hasattr(settings, 'SECURE_PROXY_SSL_HEADER') and settings.SECURE_PROXY_SSL_HEADER == ('HTTP_X_FORWARDED_PROTO', 'https'),
                   f"SECURE_PROXY_SSL_HEADER = {getattr(settings, 'SECURE_PROXY_SSL_HEADER', 'NOT SET')}"))
    
    checks.append(("Use X-Forwarded-Host", 
                   hasattr(settings, 'USE_X_FORWARDED_HOST') and settings.USE_X_FORWARDED_HOST == True,
                   f"USE_X_FORWARDED_HOST = {getattr(settings, 'USE_X_FORWARDED_HOST', 'NOT SET')}"))
    
    checks.append(("Use X-Forwarded-Port", 
                   hasattr(settings, 'USE_X_FORWARDED_PORT') and settings.USE_X_FORWARDED_PORT == True,
                   f"USE_X_FORWARDED_PORT = {getattr(settings, 'USE_X_FORWARDED_PORT', 'NOT SET')}"))
    
    # Print results
    all_passed = True
    for name, passed, detail in checks:
        status = "✅" if passed else "❌"
        print(f"{status} {name:30} {detail}")
        if not passed:
            all_passed = False
    
    print("=" * 70)
    
    if all_passed:
        print("\n✅ All security settings are properly configured!")
        print("\n📝 Summary:")
        print("   - HTTPS redirect enabled")
        print("   - HSTS configured with 1-year max-age")
        print("   - Secure cookies enabled")
        print("   - Content type sniffing prevented")
        print("   - XSS filter enabled")
        print("   - Clickjacking protection enabled")
        print("   - Proxy headers configured")
        return True
    else:
        print("\n❌ Some security settings are missing or incorrect!")
        return False

if __name__ == '__main__':
    success = verify_settings()
    sys.exit(0 if success else 1)

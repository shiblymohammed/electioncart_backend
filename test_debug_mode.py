#!/usr/bin/env python
"""
Test script to verify DEBUG mode configuration
"""
import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'election_cart.settings')

import django
django.setup()

from django.conf import settings

print("=" * 60)
print("DEBUG MODE CONFIGURATION TEST")
print("=" * 60)

# Test 1: Check DEBUG value
print(f"\n1. DEBUG Setting: {settings.DEBUG}")
print(f"   Environment Variable: {os.getenv('DEBUG', 'Not Set')}")

if settings.DEBUG:
    print("   ⚠️  WARNING: DEBUG is True")
    print("   This should only be True in development!")
else:
    print("   ✅ GOOD: DEBUG is False (production-safe)")

# Test 2: Check SECRET_KEY
print(f"\n2. SECRET_KEY: {'Set' if settings.SECRET_KEY else 'NOT SET'}")
if settings.SECRET_KEY == 'django-insecure-change-this-in-production':
    print("   ⚠️  WARNING: Using default SECRET_KEY")
else:
    print(f"   ✅ GOOD: Custom SECRET_KEY configured")

# Test 3: Check ALLOWED_HOSTS
print(f"\n3. ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
if not settings.ALLOWED_HOSTS or settings.ALLOWED_HOSTS == ['']:
    print("   ⚠️  WARNING: ALLOWED_HOSTS is empty")
else:
    print(f"   ✅ GOOD: ALLOWED_HOSTS configured")

# Test 4: Check TEMPLATES directory
print(f"\n4. Templates Directory: {settings.TEMPLATES[0]['DIRS']}")
templates_dir = Path(settings.BASE_DIR) / 'templates'
if templates_dir.exists():
    print(f"   ✅ GOOD: Templates directory exists")
    
    # Check for error pages
    error_404 = templates_dir / '404.html'
    error_500 = templates_dir / '500.html'
    
    if error_404.exists():
        print(f"   ✅ GOOD: 404.html exists")
    else:
        print(f"   ❌ ERROR: 404.html not found")
    
    if error_500.exists():
        print(f"   ✅ GOOD: 500.html exists")
    else:
        print(f"   ❌ ERROR: 500.html not found")
else:
    print(f"   ❌ ERROR: Templates directory not found")

# Test 5: Security settings (when DEBUG=False)
if not settings.DEBUG:
    print(f"\n5. Security Settings (DEBUG=False):")
    print(f"   - SECURE_SSL_REDIRECT: {getattr(settings, 'SECURE_SSL_REDIRECT', 'Not Set')}")
    print(f"   - SESSION_COOKIE_SECURE: {getattr(settings, 'SESSION_COOKIE_SECURE', 'Not Set')}")
    print(f"   - CSRF_COOKIE_SECURE: {getattr(settings, 'CSRF_COOKIE_SECURE', 'Not Set')}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)

# Summary
issues = []
if settings.DEBUG and os.getenv('DJANGO_ENVIRONMENT') == 'production':
    issues.append("DEBUG is True in production")
if settings.SECRET_KEY == 'django-insecure-change-this-in-production':
    issues.append("Using default SECRET_KEY")
if not templates_dir.exists():
    issues.append("Templates directory missing")

if issues:
    print("\n⚠️  ISSUES FOUND:")
    for issue in issues:
        print(f"   - {issue}")
    sys.exit(1)
else:
    print("\n✅ All checks passed!")
    sys.exit(0)

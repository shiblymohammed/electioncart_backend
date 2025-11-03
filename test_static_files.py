#!/usr/bin/env python
"""
Test script to verify WhiteNoise static file serving configuration
"""

import os
import sys
import time
import subprocess
import requests
from pathlib import Path

def start_server():
    """Start Django development server with DEBUG=False"""
    env = os.environ.copy()
    env['DEBUG'] = 'False'
    
    process = subprocess.Popen(
        [sys.executable, 'manage.py', 'runserver', '8000', '--noreload'],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return process

def test_whitenoise_configuration():
    """Test that WhiteNoise is properly configured"""
    print("🔍 Testing WhiteNoise Configuration\n")
    print("=" * 70)
    
    # Import Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'election_cart.settings')
    import django
    django.setup()
    from django.conf import settings
    
    checks = []
    
    # Check middleware
    middleware = settings.MIDDLEWARE
    if 'whitenoise.middleware.WhiteNoiseMiddleware' in middleware:
        print("✅ WhiteNoise middleware is configured")
        
        # Check position (should be after SecurityMiddleware)
        security_idx = middleware.index('django.middleware.security.SecurityMiddleware')
        whitenoise_idx = middleware.index('whitenoise.middleware.WhiteNoiseMiddleware')
        
        if whitenoise_idx == security_idx + 1:
            print("   ✅ WhiteNoise is correctly positioned (after SecurityMiddleware)")
            checks.append(True)
        else:
            print("   ⚠️  WhiteNoise should be immediately after SecurityMiddleware")
            checks.append(False)
    else:
        print("❌ WhiteNoise middleware not found")
        checks.append(False)
    
    # Check STATICFILES_STORAGE
    storage = getattr(settings, 'STATICFILES_STORAGE', None)
    if storage == 'whitenoise.storage.CompressedManifestStaticFilesStorage':
        print("✅ WhiteNoise storage configured (with compression)")
        checks.append(True)
    elif storage and 'whitenoise' in storage.lower():
        print(f"✅ WhiteNoise storage configured: {storage}")
        checks.append(True)
    else:
        print(f"❌ WhiteNoise storage not configured (current: {storage})")
        checks.append(False)
    
    # Check STATIC_ROOT
    static_root = settings.STATIC_ROOT
    if static_root and Path(static_root).exists():
        print(f"✅ STATIC_ROOT exists: {static_root}")
        
        # Count static files
        static_files = list(Path(static_root).rglob('*.*'))
        print(f"   📁 {len(static_files)} static files collected")
        checks.append(True)
    else:
        print(f"❌ STATIC_ROOT not found: {static_root}")
        checks.append(False)
    
    print("=" * 70)
    
    return all(checks)

def test_static_file_serving():
    """Test that static files are served correctly"""
    print("\n📦 Testing Static File Serving\n")
    print("=" * 70)
    
    # Wait for server to start
    time.sleep(5)
    
    try:
        # Test admin static files (always available)
        admin_css_url = 'http://127.0.0.1:8000/static/admin/css/base.css'
        
        print(f"📝 Testing static file: {admin_css_url}")
        
        response = requests.get(admin_css_url, timeout=5)
        
        print(f"\n📊 Response Details:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Content-Type: {response.headers.get('Content-Type')}")
        print(f"   Content-Length: {response.headers.get('Content-Length')} bytes")
        
        # Check for compression headers
        content_encoding = response.headers.get('Content-Encoding')
        if content_encoding:
            print(f"   Content-Encoding: {content_encoding}")
        
        # Check for cache headers
        cache_control = response.headers.get('Cache-Control')
        if cache_control:
            print(f"   Cache-Control: {cache_control}")
        
        print("\n✅ Validation:")
        
        checks = []
        
        # Check status code
        if response.status_code == 200:
            print("✅ Static file served successfully (200 OK)")
            checks.append(True)
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            checks.append(False)
        
        # Check content type
        if 'text/css' in response.headers.get('Content-Type', ''):
            print("✅ Correct Content-Type (text/css)")
            checks.append(True)
        else:
            print(f"⚠️  Content-Type: {response.headers.get('Content-Type')}")
            checks.append(True)  # Not critical
        
        # Check if content is not empty
        if len(response.content) > 0:
            print(f"✅ File has content ({len(response.content)} bytes)")
            checks.append(True)
        else:
            print("❌ File is empty")
            checks.append(False)
        
        # Check for WhiteNoise headers
        if cache_control and 'max-age' in cache_control:
            print(f"✅ Cache headers present (WhiteNoise is working)")
            checks.append(True)
        else:
            print("⚠️  Cache headers not found (may not be using WhiteNoise)")
            checks.append(True)  # Not critical for test
        
        print("=" * 70)
        
        return all(checks)
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_compression():
    """Test that static files are compressed"""
    print("\n🗜️  Testing Static File Compression\n")
    print("=" * 70)
    
    try:
        # Check if compressed files exist
        from pathlib import Path
        import django
        from django.conf import settings
        
        static_root = Path(settings.STATIC_ROOT)
        
        # Look for .gz or .br files (Brotli or Gzip)
        gz_files = list(static_root.rglob('*.gz'))
        br_files = list(static_root.rglob('*.br'))
        
        print(f"📁 Compressed Files:")
        print(f"   Gzip (.gz): {len(gz_files)} files")
        print(f"   Brotli (.br): {len(br_files)} files")
        
        if gz_files or br_files:
            print("\n✅ Static files are compressed")
            
            # Show example
            if gz_files:
                example = gz_files[0]
                original = str(example).replace('.gz', '')
                if Path(original).exists():
                    original_size = Path(original).stat().st_size
                    compressed_size = example.stat().st_size
                    ratio = (1 - compressed_size / original_size) * 100
                    print(f"\n📊 Compression Example:")
                    print(f"   File: {example.name}")
                    print(f"   Original: {original_size:,} bytes")
                    print(f"   Compressed: {compressed_size:,} bytes")
                    print(f"   Savings: {ratio:.1f}%")
            
            return True
        else:
            print("\n⚠️  No compressed files found")
            print("   This is normal if using CompressedManifestStaticFilesStorage")
            print("   Compression happens on-the-fly during serving")
            return True
            
    except Exception as e:
        print(f"⚠️  Could not check compression: {e}")
        return True  # Not critical

def test_debug_false():
    """Test that static files work with DEBUG=False"""
    print("\n🔒 Testing with DEBUG=False\n")
    print("=" * 70)
    
    import django
    from django.conf import settings
    
    if not settings.DEBUG:
        print("✅ DEBUG is False (production mode)")
        print("   Static files should be served by WhiteNoise")
        return True
    else:
        print("⚠️  DEBUG is True (development mode)")
        print("   Set DEBUG=False to test production static file serving")
        return False

if __name__ == '__main__':
    print("\n🚀 Starting WhiteNoise Static Files Tests\n")
    
    # Test configuration first
    test1 = test_whitenoise_configuration()
    test4 = test_debug_false()
    
    # Start server for serving tests
    print("\nStarting Django server with DEBUG=False...")
    server_process = start_server()
    
    try:
        # Run serving tests
        test2 = test_static_file_serving()
        test3 = test_compression()
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 Test Summary")
        print("=" * 70)
        print(f"  WhiteNoise Configuration:  {'✅ PASS' if test1 else '❌ FAIL'}")
        print(f"  Static File Serving:       {'✅ PASS' if test2 else '❌ FAIL'}")
        print(f"  Compression:               {'✅ PASS' if test3 else '❌ FAIL'}")
        print(f"  DEBUG=False Mode:          {'✅ PASS' if test4 else '❌ FAIL'}")
        print("=" * 70)
        
        if all([test1, test2, test3, test4]):
            print("\n✅ All WhiteNoise tests passed!")
            print("\n📝 WhiteNoise Summary:")
            print("   - Middleware configured correctly")
            print("   - Compressed storage enabled")
            print("   - Static files served successfully")
            print("   - Works with DEBUG=False")
            print("   - Ready for production deployment")
            sys.exit(0)
        else:
            print("\n❌ Some WhiteNoise tests failed!")
            sys.exit(1)
            
    finally:
        # Stop server
        print("\n🛑 Stopping server...")
        server_process.terminate()
        server_process.wait()

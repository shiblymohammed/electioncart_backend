#!/usr/bin/env python
"""
Test script to verify security headers are properly configured.
This script starts the Django server with DEBUG=False and checks the response headers.
"""

import os
import sys
import time
import subprocess
import requests
from threading import Thread

def start_server():
    """Start Django development server with DEBUG=False"""
    env = os.environ.copy()
    env['DEBUG'] = 'False'
    env['ALLOWED_HOSTS'] = 'localhost,127.0.0.1'
    
    # Start server
    process = subprocess.Popen(
        [sys.executable, 'manage.py', 'runserver', '8000', '--noreload'],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return process

def test_security_headers():
    """Test that security headers are present in the response"""
    print("🔍 Testing security headers...\n")
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        # Make a request to the server
        response = requests.get('http://127.0.0.1:8000/admin/', allow_redirects=False)
        
        print("📋 Response Headers:")
        print("-" * 60)
        
        # Expected security headers
        # Note: HSTS header only sent over HTTPS, not HTTP
        expected_headers = {
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
        }
        
        # Check each expected header
        all_passed = True
        for header, expected_value in expected_headers.items():
            actual_value = response.headers.get(header)
            if actual_value:
                if expected_value.lower() in actual_value.lower():
                    print(f"✅ {header}: {actual_value}")
                else:
                    print(f"⚠️  {header}: {actual_value} (expected: {expected_value})")
                    all_passed = False
            else:
                print(f"❌ {header}: NOT FOUND")
                all_passed = False
        
        # Check for HSTS (only present over HTTPS)
        hsts_header = response.headers.get('Strict-Transport-Security')
        if hsts_header:
            print(f"✅ Strict-Transport-Security: {hsts_header}")
        else:
            print(f"ℹ️  Strict-Transport-Security: Not present (expected over HTTP, will be present over HTTPS)")
        
        print("-" * 60)
        
        # Check for HTTPS redirect (should be 301 or 302 in production with HTTPS)
        # Note: In local testing without HTTPS, this won't redirect
        print(f"\n📊 Status Code: {response.status_code}")
        
        if all_passed:
            print("\n✅ All security headers are properly configured!")
        else:
            print("\n⚠️  Some security headers are missing or incorrect.")
        
        return all_passed
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Starting Django server with DEBUG=False...\n")
    
    # Start server in background
    server_process = start_server()
    
    try:
        # Run tests
        success = test_security_headers()
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    finally:
        # Stop server
        print("\n🛑 Stopping server...")
        server_process.terminate()
        server_process.wait()

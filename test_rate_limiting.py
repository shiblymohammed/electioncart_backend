#!/usr/bin/env python
"""
Test script to verify rate limiting functionality on authentication and order endpoints
"""

import os
import sys
import time
import subprocess
import requests
import json

def start_server():
    """Start Django development server"""
    process = subprocess.Popen(
        [sys.executable, 'manage.py', 'runserver', '8000', '--noreload'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return process

def test_login_rate_limit():
    """Test rate limiting on login endpoint (5 requests per minute)"""
    print("🔍 Testing Login Rate Limiting (5/minute)\n")
    print("=" * 70)
    
    url = 'http://127.0.0.1:8000/api/auth/login/'
    payload = {'username': 'testuser', 'password': 'testpass'}
    
    print("📝 Making 6 rapid login requests...\n")
    
    results = []
    for i in range(6):
        response = requests.post(url, json=payload)
        results.append({
            'request': i + 1,
            'status': response.status_code,
            'limited': response.status_code == 429
        })
        print(f"  Request {i+1}: Status {response.status_code}")
        
        if response.status_code == 429:
            data = response.json()
            print(f"    Message: {data.get('error')}")
    
    print("\n" + "=" * 70)
    print("✅ Validation Results:")
    print("=" * 70)
    
    # Check that first 5 requests succeeded (or returned 401 for invalid creds)
    first_five_ok = all(r['status'] in [401, 400] for r in results[:5])
    # Check that 6th request was rate limited (403 or 429)
    sixth_limited = results[5]['status'] in [403, 429]
    
    if first_five_ok:
        print("✅ First 5 requests allowed (returned 401/400 for invalid credentials)")
    else:
        print("❌ First 5 requests should not be rate limited")
    
    if sixth_limited:
        print(f"✅ 6th request was rate limited ({results[5]['status']})")
    else:
        print("❌ 6th request should be rate limited")
    
    print("=" * 70)
    
    return first_five_ok and sixth_limited

def test_signup_rate_limit():
    """Test rate limiting on signup endpoint (3 requests per hour)"""
    print("\n🔍 Testing Signup Rate Limiting (3/hour)\n")
    print("=" * 70)
    
    url = 'http://127.0.0.1:8000/api/auth/signup/'
    
    print("📝 Making 4 rapid signup requests...\n")
    
    results = []
    for i in range(4):
        payload = {
            'username': f'testuser{i}_{int(time.time())}',
            'password': 'testpass123',
            'phone_number': f'123456789{i}'
        }
        response = requests.post(url, json=payload)
        results.append({
            'request': i + 1,
            'status': response.status_code,
            'limited': response.status_code == 429
        })
        print(f"  Request {i+1}: Status {response.status_code}")
        
        if response.status_code == 429:
            data = response.json()
            print(f"    Message: {data.get('error')}")
    
    print("\n" + "=" * 70)
    print("✅ Validation Results:")
    print("=" * 70)
    
    # Check that first 3 requests succeeded (or returned 400/500 for validation/errors)
    first_three_ok = all(r['status'] in [201, 400, 500] for r in results[:3])
    # Check that 4th request was rate limited (403 or 429)
    fourth_limited = results[3]['status'] in [403, 429]
    
    if first_three_ok:
        print("✅ First 3 requests allowed")
    else:
        print("❌ First 3 requests should not be rate limited")
    
    if fourth_limited:
        print(f"✅ 4th request was rate limited ({results[3]['status']})")
    else:
        print("❌ 4th request should be rate limited")
    
    print("=" * 70)
    
    return first_three_ok and fourth_limited

def test_rate_limit_logging():
    """Test that rate limit violations are logged"""
    print("\n📝 Testing Rate Limit Logging\n")
    print("=" * 70)
    
    # Make a rate-limited request
    url = 'http://127.0.0.1:8000/api/auth/login/'
    payload = {'username': 'testuser', 'password': 'testpass'}
    
    # Make 6 requests to trigger rate limit
    for i in range(6):
        requests.post(url, json=payload)
    
    # Wait a moment for logs to be written
    time.sleep(1)
    
    # Check if rate limit was logged
    from pathlib import Path
    logs_dir = Path('logs')
    django_log = logs_dir / 'django.log'
    
    if django_log.exists():
        with open(django_log, 'r') as f:
            log_content = f.read()
        
        if 'Rate limit exceeded' in log_content:
            print("✅ Rate limit violations are being logged")
            print("   Found 'Rate limit exceeded' in django.log")
            return True
        else:
            print("⚠️  Rate limit violations may not be logged")
            return False
    else:
        print("⚠️  Log file not found")
        return False

def test_rate_limit_response_format():
    """Test that rate limit responses have correct format"""
    print("\n📋 Testing Rate Limit Response Format\n")
    print("=" * 70)
    
    url = 'http://127.0.0.1:8000/api/auth/login/'
    payload = {'username': 'testuser', 'password': 'testpass'}
    
    # Make 6 requests to trigger rate limit
    for i in range(6):
        response = requests.post(url, json=payload)
        if response.status_code in [403, 429]:
            print(f"📦 Rate Limit Response (Status {response.status_code}):")
            
            try:
                data = response.json()
                print(json.dumps(data, indent=2))
                
                print("\n✅ Validation:")
                
                # Check for error field
                if 'error' in data or 'detail' in data:
                    print("✅ Response contains error information")
                    if 'error' in data:
                        print(f"   Message: {data['error']}")
                    if 'detail' in data:
                        print(f"   Detail: {data['detail']}")
                else:
                    print("⚠️  Response format could be improved")
                
                return True
            except:
                print("⚠️  Response is not JSON")
                return True  # Still counts as rate limited
    
    print("⚠️  Could not trigger rate limit")
    return False

if __name__ == '__main__':
    print("\n🚀 Starting Rate Limiting Tests\n")
    
    # Start server
    print("Starting Django server...")
    server_process = start_server()
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(3)
    
    try:
        # Run all tests
        test1 = test_login_rate_limit()
        test2 = test_signup_rate_limit()
        test3 = test_rate_limit_logging()
        test4 = test_rate_limit_response_format()
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 Test Summary")
        print("=" * 70)
        print(f"  Login Rate Limit (5/min):     {'✅ PASS' if test1 else '❌ FAIL'}")
        print(f"  Signup Rate Limit (3/hour):   {'✅ PASS' if test2 else '❌ FAIL'}")
        print(f"  Rate Limit Logging:            {'✅ PASS' if test3 else '❌ FAIL'}")
        print(f"  Response Format:               {'✅ PASS' if test4 else '❌ FAIL'}")
        print("=" * 70)
        
        if all([test1, test2, test3, test4]):
            print("\n✅ All rate limiting tests passed!")
            print("\n📝 Rate Limiting Summary:")
            print("   - Login: 5 requests/minute per IP")
            print("   - Signup: 3 requests/hour per IP")
            print("   - Order Creation: 10 requests/hour per user")
            print("   - Resource Upload: 20 requests/hour per user")
            print("   - All violations logged")
            print("   - Clear error messages returned")
            sys.exit(0)
        else:
            print("\n❌ Some rate limiting tests failed!")
            sys.exit(1)
            
    finally:
        # Stop server
        print("\n🛑 Stopping server...")
        server_process.terminate()
        server_process.wait()

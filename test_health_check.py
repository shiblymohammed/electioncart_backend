#!/usr/bin/env python
"""
Test script to verify health check endpoint functionality
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

def test_health_check_healthy():
    """Test health check when database is connected"""
    print("🔍 Testing Health Check Endpoint (Healthy State)\n")
    print("=" * 70)
    
    try:
        # Make request to health endpoint
        response = requests.get('http://127.0.0.1:8000/health/')
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📋 Response Headers:")
        print(f"   Content-Type: {response.headers.get('Content-Type')}")
        
        # Parse JSON response
        data = response.json()
        
        print(f"\n📦 Response Body:")
        print(json.dumps(data, indent=2))
        
        print("\n" + "=" * 70)
        print("✅ Validation Results:")
        print("=" * 70)
        
        # Validate response
        checks = []
        
        # Check status code
        if response.status_code == 200:
            print("✅ Status code is 200 (OK)")
            checks.append(True)
        else:
            print(f"❌ Status code is {response.status_code} (expected 200)")
            checks.append(False)
        
        # Check content type
        if 'application/json' in response.headers.get('Content-Type', ''):
            print("✅ Content-Type is application/json")
            checks.append(True)
        else:
            print(f"❌ Content-Type is {response.headers.get('Content-Type')}")
            checks.append(False)
        
        # Check required fields
        required_fields = ['status', 'service', 'database', 'timestamp']
        for field in required_fields:
            if field in data:
                print(f"✅ Field '{field}' present: {data[field]}")
                checks.append(True)
            else:
                print(f"❌ Field '{field}' missing")
                checks.append(False)
        
        # Check status value
        if data.get('status') == 'healthy':
            print("✅ Status is 'healthy'")
            checks.append(True)
        else:
            print(f"❌ Status is '{data.get('status')}' (expected 'healthy')")
            checks.append(False)
        
        # Check database value
        if data.get('database') == 'connected':
            print("✅ Database is 'connected'")
            checks.append(True)
        else:
            print(f"❌ Database is '{data.get('database')}' (expected 'connected')")
            checks.append(False)
        
        # Check service name
        if data.get('service') == 'election-cart-api':
            print("✅ Service name is 'election-cart-api'")
            checks.append(True)
        else:
            print(f"❌ Service name is '{data.get('service')}'")
            checks.append(False)
        
        # Check timestamp format
        if data.get('timestamp') and 'T' in data.get('timestamp', ''):
            print(f"✅ Timestamp is in ISO format: {data.get('timestamp')}")
            checks.append(True)
        else:
            print(f"❌ Timestamp format invalid: {data.get('timestamp')}")
            checks.append(False)
        
        print("=" * 70)
        
        return all(checks)
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return False
    except json.JSONDecodeError:
        print("❌ Response is not valid JSON")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_health_check_no_auth():
    """Test that health check doesn't require authentication"""
    print("\n🔓 Testing Health Check Without Authentication\n")
    print("=" * 70)
    
    try:
        # Make request without any authentication headers
        response = requests.get('http://127.0.0.1:8000/health/')
        
        if response.status_code == 200:
            print("✅ Health check accessible without authentication")
            print(f"   Status: {response.status_code}")
            return True
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_health_check_response_time():
    """Test that health check responds quickly"""
    print("\n⏱️  Testing Health Check Response Time\n")
    print("=" * 70)
    
    try:
        # Measure response time
        start_time = time.time()
        response = requests.get('http://127.0.0.1:8000/health/')
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        print(f"📊 Response Time: {response_time:.2f}ms")
        
        if response_time < 1000:  # Less than 1 second
            print(f"✅ Response time is acceptable (< 1000ms)")
            return True
        else:
            print(f"⚠️  Response time is slow (> 1000ms)")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_health_check_multiple_requests():
    """Test that health check handles multiple rapid requests"""
    print("\n🔄 Testing Multiple Rapid Requests\n")
    print("=" * 70)
    
    try:
        num_requests = 10
        print(f"📝 Making {num_requests} rapid requests...")
        
        success_count = 0
        for i in range(num_requests):
            response = requests.get('http://127.0.0.1:8000/health/')
            if response.status_code == 200:
                success_count += 1
        
        print(f"\n📊 Results: {success_count}/{num_requests} successful")
        
        if success_count == num_requests:
            print("✅ All requests succeeded")
            return True
        else:
            print(f"⚠️  {num_requests - success_count} requests failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    print("\n🚀 Starting Health Check Tests\n")
    
    # Start server
    print("Starting Django server...")
    server_process = start_server()
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(3)
    
    try:
        # Run all tests
        test1 = test_health_check_healthy()
        test2 = test_health_check_no_auth()
        test3 = test_health_check_response_time()
        test4 = test_health_check_multiple_requests()
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 Test Summary")
        print("=" * 70)
        print(f"  Healthy State Test:      {'✅ PASS' if test1 else '❌ FAIL'}")
        print(f"  No Auth Required Test:   {'✅ PASS' if test2 else '❌ FAIL'}")
        print(f"  Response Time Test:      {'✅ PASS' if test3 else '❌ FAIL'}")
        print(f"  Multiple Requests Test:  {'✅ PASS' if test4 else '❌ FAIL'}")
        print("=" * 70)
        
        if all([test1, test2, test3, test4]):
            print("\n✅ All health check tests passed!")
            print("\n📝 Health Check Endpoint Ready:")
            print("   - URL: http://localhost:8000/health/")
            print("   - No authentication required")
            print("   - Returns JSON with system status")
            print("   - Response time < 1 second")
            print("   - Ready for monitoring integration")
            sys.exit(0)
        else:
            print("\n❌ Some health check tests failed!")
            sys.exit(1)
            
    finally:
        # Stop server
        print("\n🛑 Stopping server...")
        server_process.terminate()
        server_process.wait()

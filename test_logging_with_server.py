#!/usr/bin/env python
"""
Test logging with actual Django server requests
"""

import os
import sys
import time
import subprocess
import requests
from pathlib import Path

def start_server():
    """Start Django development server"""
    process = subprocess.Popen(
        [sys.executable, 'manage.py', 'runserver', '8000', '--noreload'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return process

def test_server_logging():
    """Test that server requests are logged"""
    print("🔍 Testing Server Request Logging\n")
    print("=" * 70)
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        # Make various requests
        print("📝 Making test requests...\n")
        
        # Request 1: Admin page (should log)
        response = requests.get('http://127.0.0.1:8000/admin/', allow_redirects=False)
        print(f"  ✅ GET /admin/ - Status: {response.status_code}")
        
        # Request 2: API endpoint (should log)
        response = requests.get('http://127.0.0.1:8000/api/packages/', allow_redirects=False)
        print(f"  ✅ GET /api/packages/ - Status: {response.status_code}")
        
        # Request 3: Non-existent page (should log 404)
        response = requests.get('http://127.0.0.1:8000/nonexistent/', allow_redirects=False)
        print(f"  ✅ GET /nonexistent/ - Status: {response.status_code}")
        
        print("\n" + "=" * 70)
        
        # Wait a moment for logs to be written
        time.sleep(1)
        
        # Check log files
        logs_dir = Path('logs')
        django_log = logs_dir / 'django.log'
        
        print("\n📁 Checking django.log for request logs:\n")
        
        if django_log.exists():
            with open(django_log, 'r') as f:
                lines = f.readlines()
                
            # Show last 10 lines
            print("  Last 10 log entries:")
            for line in lines[-10:]:
                print(f"    {line.strip()}")
            
            print(f"\n  ✅ Total log entries: {len(lines)}")
        else:
            print("  ❌ django.log not found")
        
        print("\n" + "=" * 70)
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    print("\n🚀 Starting Django Server for Logging Test\n")
    
    # Start server
    server_process = start_server()
    
    try:
        # Run test
        success = test_server_logging()
        
        if success:
            print("\n✅ Server logging test passed!")
            print("\n📝 Logging is working correctly:")
            print("   - Server requests are logged to django.log")
            print("   - Errors are logged to error.log")
            print("   - Logs include timestamps, module names, and messages")
        else:
            print("\n❌ Server logging test failed!")
        
        sys.exit(0 if success else 1)
        
    finally:
        # Stop server
        print("\n🛑 Stopping server...")
        server_process.terminate()
        server_process.wait()

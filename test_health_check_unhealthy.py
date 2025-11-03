#!/usr/bin/env python
"""
Test script to verify health check endpoint returns 503 when database is down.
This test simulates a database failure by temporarily breaking the connection.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'election_cart.settings')
django.setup()

from django.test import RequestFactory
from django.db import connection
from election_cart.urls import health_check
import json

def test_health_check_with_db_error():
    """Test health check when database connection fails"""
    print("🔍 Testing Health Check with Database Error\n")
    print("=" * 70)
    
    # Create a mock request
    factory = RequestFactory()
    request = factory.get('/health/')
    
    # Temporarily close the database connection to simulate failure
    print("📝 Simulating database connection failure...")
    
    # Save original database settings
    from django.conf import settings
    original_db = settings.DATABASES['default'].copy()
    
    try:
        # Break the database connection by using invalid credentials
        settings.DATABASES['default']['NAME'] = 'nonexistent_database_12345'
        
        # Force close existing connections
        connection.close()
        
        # Call health check
        response = health_check(request)
        
        print(f"\n📊 Response Status: {response.status_code}")
        
        # Parse response
        response_data = json.loads(response.content.decode('utf-8'))
        
        print(f"📦 Response Body:")
        print(json.dumps(response_data, indent=2))
        
        print("\n" + "=" * 70)
        print("✅ Validation Results:")
        print("=" * 70)
        
        # Validate response
        checks = []
        
        # Check status code
        if response.status_code == 503:
            print("✅ Status code is 503 (Service Unavailable)")
            checks.append(True)
        else:
            print(f"❌ Status code is {response.status_code} (expected 503)")
            checks.append(False)
        
        # Check status field
        if response_data.get('status') == 'unhealthy':
            print("✅ Status is 'unhealthy'")
            checks.append(True)
        else:
            print(f"❌ Status is '{response_data.get('status')}' (expected 'unhealthy')")
            checks.append(False)
        
        # Check database field
        if response_data.get('database') == 'disconnected':
            print("✅ Database is 'disconnected'")
            checks.append(True)
        else:
            print(f"❌ Database is '{response_data.get('database')}' (expected 'disconnected')")
            checks.append(False)
        
        # Check error field exists
        if 'error' in response_data:
            print(f"✅ Error field present: {response_data['error'][:50]}...")
            checks.append(True)
        else:
            print("❌ Error field missing")
            checks.append(False)
        
        # Check service name
        if response_data.get('service') == 'election-cart-api':
            print("✅ Service name is 'election-cart-api'")
            checks.append(True)
        else:
            print(f"❌ Service name is '{response_data.get('service')}'")
            checks.append(False)
        
        # Check timestamp
        if response_data.get('timestamp'):
            print(f"✅ Timestamp present: {response_data.get('timestamp')}")
            checks.append(True)
        else:
            print("❌ Timestamp missing")
            checks.append(False)
        
        print("=" * 70)
        
        return all(checks)
        
    finally:
        # Restore original database settings
        print("\n🔄 Restoring database connection...")
        settings.DATABASES['default'] = original_db
        connection.close()
        
        # Verify connection is restored
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            print("✅ Database connection restored")
        except Exception as e:
            print(f"⚠️  Warning: Could not restore database connection: {e}")

if __name__ == '__main__':
    print("\n🚀 Starting Health Check Unhealthy State Test\n")
    
    try:
        success = test_health_check_with_db_error()
        
        print("\n" + "=" * 70)
        print("📊 Test Summary")
        print("=" * 70)
        print(f"  Unhealthy State Test: {'✅ PASS' if success else '❌ FAIL'}")
        print("=" * 70)
        
        if success:
            print("\n✅ Health check correctly returns 503 when database is down!")
            print("\n📝 Verified Behavior:")
            print("   - Returns 503 status code")
            print("   - Status field is 'unhealthy'")
            print("   - Database field is 'disconnected'")
            print("   - Error message included")
            print("   - Monitoring systems can detect failures")
            sys.exit(0)
        else:
            print("\n❌ Health check unhealthy state test failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

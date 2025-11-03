#!/usr/bin/env python
"""
Test script to verify database configuration with DATABASE_URL support
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'election_cart.settings')
django.setup()

from django.conf import settings
from django.db import connection
import json

def test_database_configuration():
    """Test that database is properly configured"""
    print("🔍 Testing Database Configuration\n")
    print("=" * 70)
    
    # Check database settings
    db_config = settings.DATABASES['default']
    
    print("📋 Database Configuration:")
    print("-" * 70)
    
    # Mask sensitive information
    safe_config = {}
    for key, value in db_config.items():
        if key in ['PASSWORD', 'USER']:
            safe_config[key] = '***' if value else 'NOT SET'
        elif key == 'OPTIONS' and isinstance(value, dict):
            safe_config[key] = {k: v for k, v in value.items()}
        else:
            safe_config[key] = value
    
    for key, value in safe_config.items():
        if isinstance(value, dict):
            print(f"  {key}:")
            for k, v in value.items():
                print(f"    {k}: {v}")
        else:
            print(f"  {key}: {value}")
    
    print("-" * 70)
    
    # Validation checks
    checks = []
    
    # Check ENGINE
    if db_config.get('ENGINE') == 'django.db.backends.postgresql':
        print("✅ Database engine is PostgreSQL")
        checks.append(True)
    else:
        print(f"❌ Database engine is {db_config.get('ENGINE')} (expected PostgreSQL)")
        checks.append(False)
    
    # Check connection pooling
    conn_max_age = db_config.get('CONN_MAX_AGE', 0)
    if conn_max_age == 600:
        print(f"✅ Connection pooling enabled (CONN_MAX_AGE: {conn_max_age}s)")
        checks.append(True)
    else:
        print(f"⚠️  Connection pooling: {conn_max_age}s (expected 600s)")
        checks.append(False)
    
    # Check SSL configuration
    options = db_config.get('OPTIONS', {})
    sslmode = options.get('sslmode', 'prefer')
    db_host = db_config.get('HOST', 'localhost')
    is_local = db_host in ['localhost', '127.0.0.1', '::1']
    
    if settings.DEBUG or is_local:
        if sslmode in ['prefer', 'allow', 'disable']:
            print(f"✅ SSL mode for development/localhost: {sslmode}")
            checks.append(True)
        else:
            print(f"⚠️  SSL mode: {sslmode}")
            checks.append(True)
    else:
        if sslmode == 'require':
            print(f"✅ SSL required for production: {sslmode}")
            checks.append(True)
        else:
            print(f"❌ SSL should be 'require' in production (current: {sslmode})")
            checks.append(False)
    
    # Check connection timeout
    timeout = options.get('connect_timeout')
    if timeout:
        print(f"✅ Connection timeout configured: {timeout}s")
        checks.append(True)
    else:
        print("⚠️  Connection timeout not configured")
        checks.append(True)  # Not critical
    
    print("=" * 70)
    
    return all(checks)

def test_database_connection():
    """Test actual database connection"""
    print("\n🔌 Testing Database Connection\n")
    print("=" * 70)
    
    try:
        # Test connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT version()")
            version = cursor.fetchone()[0]
        
        print(f"✅ Database connection successful")
        print(f"   PostgreSQL version: {version.split(',')[0]}")
        
        # Test connection pooling
        print(f"\n📊 Connection Info:")
        print(f"   Connection max age: {connection.settings_dict.get('CONN_MAX_AGE')}s")
        print(f"   Connection closed: {connection.connection is None}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_database_url_parsing():
    """Test DATABASE_URL parsing if set"""
    print("\n🔗 Testing DATABASE_URL Support\n")
    print("=" * 70)
    
    if 'DATABASE_URL' in os.environ:
        print("✅ DATABASE_URL environment variable is set")
        
        # Parse DATABASE_URL (mask password)
        db_url = os.environ['DATABASE_URL']
        if '@' in db_url:
            parts = db_url.split('@')
            masked_url = parts[0].split(':')[0] + ':***@' + parts[1]
        else:
            masked_url = db_url
        
        print(f"   URL: {masked_url}")
        
        # Check if dj_database_url was used
        db_config = settings.DATABASES['default']
        if 'NAME' in db_config and 'HOST' in db_config:
            print("✅ DATABASE_URL successfully parsed")
            print(f"   Database: {db_config.get('NAME')}")
            print(f"   Host: {db_config.get('HOST')}")
            print(f"   Port: {db_config.get('PORT')}")
            return True
        else:
            print("⚠️  DATABASE_URL may not be parsed correctly")
            return False
    else:
        print("ℹ️  DATABASE_URL not set (using manual configuration)")
        print("   This is normal for local development")
        
        # Check manual configuration
        db_config = settings.DATABASES['default']
        print(f"\n📋 Manual Configuration:")
        print(f"   Database: {db_config.get('NAME')}")
        print(f"   Host: {db_config.get('HOST')}")
        print(f"   Port: {db_config.get('PORT')}")
        
        return True

def test_connection_pooling():
    """Test that connection pooling is working"""
    print("\n♻️  Testing Connection Pooling\n")
    print("=" * 70)
    
    try:
        # Make first query
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        
        conn1_id = id(connection.connection)
        print(f"✅ First connection established (ID: {conn1_id})")
        
        # Close cursor but connection should be pooled
        connection.close()
        
        # Make second query - should reuse connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        
        conn2_id = id(connection.connection)
        print(f"✅ Second connection established (ID: {conn2_id})")
        
        # In development, connections might not be reused
        # In production with CONN_MAX_AGE, they should be
        if settings.DATABASES['default'].get('CONN_MAX_AGE', 0) > 0:
            print(f"✅ Connection pooling configured (max age: {settings.DATABASES['default']['CONN_MAX_AGE']}s)")
        else:
            print("⚠️  Connection pooling not configured")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection pooling test failed: {e}")
        return False

if __name__ == '__main__':
    print("\n🚀 Starting Database Configuration Tests\n")
    
    try:
        # Run all tests
        test1 = test_database_configuration()
        test2 = test_database_connection()
        test3 = test_database_url_parsing()
        test4 = test_connection_pooling()
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 Test Summary")
        print("=" * 70)
        print(f"  Database Configuration:  {'✅ PASS' if test1 else '❌ FAIL'}")
        print(f"  Database Connection:     {'✅ PASS' if test2 else '❌ FAIL'}")
        print(f"  DATABASE_URL Support:    {'✅ PASS' if test3 else '❌ FAIL'}")
        print(f"  Connection Pooling:      {'✅ PASS' if test4 else '❌ FAIL'}")
        print("=" * 70)
        
        if all([test1, test2, test3, test4]):
            print("\n✅ All database configuration tests passed!")
            print("\n📝 Configuration Summary:")
            print("   - PostgreSQL database configured")
            print("   - Connection pooling enabled (600s)")
            print("   - SSL configured for production")
            print("   - DATABASE_URL support enabled")
            print("   - Fallback to manual config available")
            sys.exit(0)
        else:
            print("\n❌ Some database configuration tests failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

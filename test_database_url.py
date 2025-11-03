#!/usr/bin/env python
"""
Test DATABASE_URL parsing functionality
"""

import os
import sys

# Set a test DATABASE_URL before importing Django
os.environ['DATABASE_URL'] = 'postgresql://testuser:testpass@testhost:5432/testdb'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'election_cart.settings')

import django
django.setup()

from django.conf import settings

def test_database_url_parsing():
    """Test that DATABASE_URL is correctly parsed"""
    print("🔗 Testing DATABASE_URL Parsing\n")
    print("=" * 70)
    
    db_config = settings.DATABASES['default']
    
    print("📋 Parsed Configuration:")
    print("-" * 70)
    
    # Check parsed values
    checks = []
    
    # Check database name
    if db_config.get('NAME') == 'testdb':
        print(f"✅ Database name: {db_config.get('NAME')}")
        checks.append(True)
    else:
        print(f"❌ Database name: {db_config.get('NAME')} (expected: testdb)")
        checks.append(False)
    
    # Check host
    if db_config.get('HOST') == 'testhost':
        print(f"✅ Host: {db_config.get('HOST')}")
        checks.append(True)
    else:
        print(f"❌ Host: {db_config.get('HOST')} (expected: testhost)")
        checks.append(False)
    
    # Check port
    if db_config.get('PORT') == 5432:
        print(f"✅ Port: {db_config.get('PORT')}")
        checks.append(True)
    else:
        print(f"❌ Port: {db_config.get('PORT')} (expected: 5432)")
        checks.append(False)
    
    # Check user
    if db_config.get('USER') == 'testuser':
        print(f"✅ User: {db_config.get('USER')}")
        checks.append(True)
    else:
        print(f"❌ User: {db_config.get('USER')} (expected: testuser)")
        checks.append(False)
    
    # Check password (don't print it)
    if db_config.get('PASSWORD') == 'testpass':
        print(f"✅ Password: *** (correctly parsed)")
        checks.append(True)
    else:
        print(f"❌ Password not correctly parsed")
        checks.append(False)
    
    # Check connection pooling
    if db_config.get('CONN_MAX_AGE') == 600:
        print(f"✅ Connection pooling: {db_config.get('CONN_MAX_AGE')}s")
        checks.append(True)
    else:
        print(f"❌ Connection pooling: {db_config.get('CONN_MAX_AGE')} (expected: 600)")
        checks.append(False)
    
    # Check engine
    if db_config.get('ENGINE') == 'django.db.backends.postgresql':
        print(f"✅ Engine: PostgreSQL")
        checks.append(True)
    else:
        print(f"❌ Engine: {db_config.get('ENGINE')}")
        checks.append(False)
    
    print("-" * 70)
    
    if all(checks):
        print("\n✅ DATABASE_URL parsing successful!")
        print("\n📝 Summary:")
        print("   - DATABASE_URL correctly parsed")
        print("   - All connection parameters extracted")
        print("   - Connection pooling configured")
        print("   - Ready for production deployment")
        return True
    else:
        print("\n❌ DATABASE_URL parsing failed!")
        return False

if __name__ == '__main__':
    print("\n🚀 Testing DATABASE_URL Support\n")
    
    try:
        success = test_database_url_parsing()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

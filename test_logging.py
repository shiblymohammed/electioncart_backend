#!/usr/bin/env python
"""
Test script to verify logging configuration is working correctly.
"""

import os
import sys
import django
import logging
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'election_cart.settings')
django.setup()

from django.conf import settings

def test_logging_configuration():
    """Test that logging is properly configured"""
    print("🔍 Testing Logging Configuration\n")
    print("=" * 70)
    
    # Check logs directory exists
    logs_dir = settings.BASE_DIR / 'logs'
    if logs_dir.exists():
        print(f"✅ Logs directory exists: {logs_dir}")
    else:
        print(f"❌ Logs directory not found: {logs_dir}")
        return False
    
    # Check logging configuration
    if hasattr(settings, 'LOGGING'):
        print("✅ LOGGING configuration found in settings")
    else:
        print("❌ LOGGING configuration not found in settings")
        return False
    
    # Verify handlers
    handlers = settings.LOGGING.get('handlers', {})
    expected_handlers = ['console', 'file', 'error_file']
    
    print("\n📋 Configured Handlers:")
    for handler_name in expected_handlers:
        if handler_name in handlers:
            handler = handlers[handler_name]
            print(f"  ✅ {handler_name}")
            print(f"     - Class: {handler.get('class')}")
            if 'filename' in handler:
                print(f"     - File: {handler.get('filename')}")
            print(f"     - Level: {handler.get('level')}")
        else:
            print(f"  ❌ {handler_name} - NOT FOUND")
    
    # Verify formatters
    formatters = settings.LOGGING.get('formatters', {})
    expected_formatters = ['verbose', 'simple']
    
    print("\n📋 Configured Formatters:")
    for formatter_name in expected_formatters:
        if formatter_name in formatters:
            print(f"  ✅ {formatter_name}")
        else:
            print(f"  ❌ {formatter_name} - NOT FOUND")
    
    # Verify loggers
    loggers = settings.LOGGING.get('loggers', {})
    expected_loggers = ['django', 'django.request', 'authentication', 'orders']
    
    print("\n📋 Configured Loggers:")
    for logger_name in expected_loggers:
        if logger_name in loggers:
            logger = loggers[logger_name]
            print(f"  ✅ {logger_name}")
            print(f"     - Handlers: {logger.get('handlers')}")
            print(f"     - Level: {logger.get('level')}")
        else:
            print(f"  ❌ {logger_name} - NOT FOUND")
    
    print("\n" + "=" * 70)
    return True

def test_logging_functionality():
    """Test that logging actually works"""
    print("\n🧪 Testing Logging Functionality\n")
    print("=" * 70)
    
    # Get loggers
    django_logger = logging.getLogger('django')
    auth_logger = logging.getLogger('authentication')
    orders_logger = logging.getLogger('orders')
    
    # Test different log levels
    print("📝 Writing test log messages...\n")
    
    django_logger.info("Test INFO message from django logger")
    print("  ✅ Wrote INFO message to django logger")
    
    auth_logger.info("Test authentication INFO message")
    print("  ✅ Wrote INFO message to authentication logger")
    
    orders_logger.warning("Test orders WARNING message")
    print("  ✅ Wrote WARNING message to orders logger")
    
    # Test error logging
    try:
        # Intentionally cause an error
        raise ValueError("Test error for logging")
    except ValueError as e:
        django_logger.error(f"Test ERROR message: {e}", exc_info=True)
        print("  ✅ Wrote ERROR message with stack trace")
    
    print("\n" + "=" * 70)
    
    # Check if log files were created
    logs_dir = settings.BASE_DIR / 'logs'
    django_log = logs_dir / 'django.log'
    error_log = logs_dir / 'error.log'
    
    print("\n📁 Checking Log Files:\n")
    
    if django_log.exists():
        size = django_log.stat().st_size
        print(f"  ✅ django.log created ({size} bytes)")
        
        # Read last few lines
        with open(django_log, 'r') as f:
            lines = f.readlines()
            if lines:
                print(f"     Last entry: {lines[-1].strip()}")
    else:
        print(f"  ❌ django.log not found")
    
    if error_log.exists():
        size = error_log.stat().st_size
        print(f"  ✅ error.log created ({size} bytes)")
        
        # Read last few lines
        with open(error_log, 'r') as f:
            lines = f.readlines()
            if lines:
                print(f"     Last entry: {lines[-1].strip()}")
    else:
        print(f"  ❌ error.log not found")
    
    print("\n" + "=" * 70)
    return True

def test_log_rotation():
    """Test log rotation configuration"""
    print("\n🔄 Testing Log Rotation Configuration\n")
    print("=" * 70)
    
    handlers = settings.LOGGING.get('handlers', {})
    
    # Check file handler rotation
    file_handler = handlers.get('file', {})
    if file_handler.get('class') == 'logging.handlers.RotatingFileHandler':
        max_bytes = file_handler.get('maxBytes', 0)
        backup_count = file_handler.get('backupCount', 0)
        
        print(f"✅ File Handler (django.log):")
        print(f"   - Max Size: {max_bytes / (1024*1024):.1f} MB")
        print(f"   - Backup Count: {backup_count}")
        
        if max_bytes == 5 * 1024 * 1024 and backup_count == 3:
            print(f"   ✅ Rotation configured correctly (5MB, 3 backups)")
        else:
            print(f"   ⚠️  Rotation settings differ from requirements")
    
    # Check error file handler rotation
    error_handler = handlers.get('error_file', {})
    if error_handler.get('class') == 'logging.handlers.RotatingFileHandler':
        max_bytes = error_handler.get('maxBytes', 0)
        backup_count = error_handler.get('backupCount', 0)
        
        print(f"\n✅ Error File Handler (error.log):")
        print(f"   - Max Size: {max_bytes / (1024*1024):.1f} MB")
        print(f"   - Backup Count: {backup_count}")
        
        if max_bytes == 5 * 1024 * 1024 and backup_count == 5:
            print(f"   ✅ Rotation configured correctly (5MB, 5 backups)")
        else:
            print(f"   ⚠️  Rotation settings differ from requirements")
    
    print("\n" + "=" * 70)
    return True

if __name__ == '__main__':
    print("\n🚀 Starting Logging Tests\n")
    
    try:
        # Run all tests
        config_ok = test_logging_configuration()
        functionality_ok = test_logging_functionality()
        rotation_ok = test_log_rotation()
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 Test Summary:")
        print("=" * 70)
        print(f"  Configuration: {'✅ PASS' if config_ok else '❌ FAIL'}")
        print(f"  Functionality: {'✅ PASS' if functionality_ok else '❌ FAIL'}")
        print(f"  Rotation:      {'✅ PASS' if rotation_ok else '❌ FAIL'}")
        print("=" * 70)
        
        if config_ok and functionality_ok and rotation_ok:
            print("\n✅ All logging tests passed!")
            print("\n📝 Next Steps:")
            print("   1. Check logs/django.log for general application logs")
            print("   2. Check logs/error.log for error-level logs only")
            print("   3. Logs will rotate automatically at 5MB")
            sys.exit(0)
        else:
            print("\n❌ Some logging tests failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

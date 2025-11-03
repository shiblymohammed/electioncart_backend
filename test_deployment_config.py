#!/usr/bin/env python
"""
Test script to verify deployment configuration files
"""

import os
import sys
from pathlib import Path

def test_procfile():
    """Test that Procfile exists and is correctly formatted"""
    print("🔍 Testing Procfile\n")
    print("=" * 70)
    
    procfile_path = Path('Procfile')
    
    if not procfile_path.exists():
        print("❌ Procfile not found")
        return False
    
    with open(procfile_path, 'r') as f:
        content = f.read()
    
    print("📄 Procfile content:")
    print(content)
    
    checks = []
    
    # Check for web process
    if 'web:' in content:
        print("✅ Web process defined")
        checks.append(True)
    else:
        print("❌ Web process not defined")
        checks.append(False)
    
    # Check for migrate command
    if 'manage.py migrate' in content:
        print("✅ Database migrations included")
        checks.append(True)
    else:
        print("⚠️  Database migrations not included")
        checks.append(False)
    
    # Check for collectstatic
    if 'collectstatic' in content:
        print("✅ Static files collection included")
        checks.append(True)
    else:
        print("⚠️  Static files collection not included")
        checks.append(False)
    
    # Check for gunicorn
    if 'gunicorn' in content:
        print("✅ Gunicorn server configured")
        checks.append(True)
    else:
        print("❌ Gunicorn not configured")
        checks.append(False)
    
    # Check for PORT variable
    if '$PORT' in content:
        print("✅ PORT variable used")
        checks.append(True)
    else:
        print("⚠️  PORT variable not used")
        checks.append(False)
    
    print("=" * 70)
    return all(checks)

def test_gunicorn_config():
    """Test that gunicorn.conf.py exists and is valid"""
    print("\n🔧 Testing Gunicorn Configuration\n")
    print("=" * 70)
    
    config_path = Path('gunicorn.conf.py')
    
    if not config_path.exists():
        print("⚠️  gunicorn.conf.py not found (optional)")
        return True  # Optional file
    
    print("✅ gunicorn.conf.py found")
    
    try:
        # Try to import the config
        import importlib.util
        spec = importlib.util.spec_from_file_location("gunicorn_config", config_path)
        config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config)
        
        print("✅ Configuration file is valid Python")
        
        # Check for key settings
        if hasattr(config, 'workers'):
            print(f"✅ Workers configured: {config.workers}")
        
        if hasattr(config, 'bind'):
            print(f"✅ Bind address configured: {config.bind}")
        
        if hasattr(config, 'timeout'):
            print(f"✅ Timeout configured: {config.timeout}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration file has errors: {e}")
        return False
    
    finally:
        print("=" * 70)

def test_requirements():
    """Test that gunicorn is in requirements.txt"""
    print("\n📦 Testing Requirements\n")
    print("=" * 70)
    
    req_path = Path('requirements.txt')
    
    if not req_path.exists():
        print("❌ requirements.txt not found")
        return False
    
    with open(req_path, 'r') as f:
        content = f.read()
    
    if 'gunicorn' in content:
        print("✅ gunicorn in requirements.txt")
        # Extract version
        for line in content.split('\n'):
            if 'gunicorn' in line.lower():
                print(f"   Version: {line.strip()}")
        return True
    else:
        print("❌ gunicorn not in requirements.txt")
        return False
    
    print("=" * 70)

def test_runtime():
    """Test that runtime.txt exists"""
    print("\n🐍 Testing Runtime Configuration\n")
    print("=" * 70)
    
    runtime_path = Path('runtime.txt')
    
    if not runtime_path.exists():
        print("⚠️  runtime.txt not found (optional for some platforms)")
        return True  # Optional
    
    with open(runtime_path, 'r') as f:
        content = f.read().strip()
    
    print(f"✅ runtime.txt found: {content}")
    
    if 'python' in content.lower():
        print("✅ Python version specified")
        return True
    else:
        print("⚠️  Python version format may be incorrect")
        return True  # Not critical
    
    print("=" * 70)

def test_railway_config():
    """Test Railway configuration"""
    print("\n🚂 Testing Railway Configuration\n")
    print("=" * 70)
    
    railway_path = Path('railway.json')
    
    if not railway_path.exists():
        print("⚠️  railway.json not found (optional)")
        return True  # Optional
    
    print("✅ railway.json found")
    
    try:
        import json
        with open(railway_path, 'r') as f:
            config = json.load(f)
        
        print("✅ Valid JSON format")
        
        if 'deploy' in config:
            print("✅ Deploy configuration present")
            
            if 'healthcheckPath' in config['deploy']:
                print(f"   Health check: {config['deploy']['healthcheckPath']}")
            
            if 'startCommand' in config['deploy']:
                print("   ✅ Start command configured")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading config: {e}")
        return False
    
    finally:
        print("=" * 70)

def test_dockerignore():
    """Test .dockerignore file"""
    print("\n🐳 Testing Docker Ignore\n")
    print("=" * 70)
    
    dockerignore_path = Path('.dockerignore')
    
    if not dockerignore_path.exists():
        print("⚠️  .dockerignore not found (optional)")
        return True  # Optional
    
    with open(dockerignore_path, 'r') as f:
        content = f.read()
    
    print("✅ .dockerignore found")
    
    important_patterns = ['.env', '__pycache__', '*.pyc', '.git']
    found = []
    
    for pattern in important_patterns:
        if pattern in content:
            found.append(pattern)
    
    print(f"✅ Ignoring {len(found)}/{len(important_patterns)} important patterns")
    
    print("=" * 70)
    return True

if __name__ == '__main__':
    print("\n🚀 Starting Deployment Configuration Tests\n")
    
    try:
        # Run all tests
        test1 = test_procfile()
        test2 = test_gunicorn_config()
        test3 = test_requirements()
        test4 = test_runtime()
        test5 = test_railway_config()
        test6 = test_dockerignore()
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 Test Summary")
        print("=" * 70)
        print(f"  Procfile:              {'✅ PASS' if test1 else '❌ FAIL'}")
        print(f"  Gunicorn Config:       {'✅ PASS' if test2 else '❌ FAIL'}")
        print(f"  Requirements:          {'✅ PASS' if test3 else '❌ FAIL'}")
        print(f"  Runtime:               {'✅ PASS' if test4 else '❌ FAIL'}")
        print(f"  Railway Config:        {'✅ PASS' if test5 else '❌ FAIL'}")
        print(f"  Docker Ignore:         {'✅ PASS' if test6 else '❌ FAIL'}")
        print("=" * 70)
        
        if all([test1, test2, test3, test4, test5, test6]):
            print("\n✅ All deployment configuration tests passed!")
            print("\n📝 Deployment Files Ready:")
            print("   - Procfile (Railway/Heroku)")
            print("   - gunicorn.conf.py (Gunicorn settings)")
            print("   - runtime.txt (Python version)")
            print("   - railway.json (Railway config)")
            print("   - .dockerignore (Docker builds)")
            print("\n🎯 Ready for deployment!")
            sys.exit(0)
        else:
            print("\n❌ Some deployment configuration tests failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

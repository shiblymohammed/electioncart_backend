#!/usr/bin/env python
"""
Comprehensive security and deployment checks
Run before deploying to production
"""

import os
import sys
import subprocess

def run_django_check():
    """Run Django's deployment check"""
    print("🔍 Running Django Deployment Check\n")
    print("=" * 70)
    
    # Set DEBUG=False for production checks
    env = os.environ.copy()
    env['DEBUG'] = 'False'
    
    try:
        result = subprocess.run(
            [sys.executable, 'manage.py', 'check', '--deploy'],
            env=env,
            capture_output=True,
            text=True
        )
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ Django deployment check passed")
            return True
        else:
            print("❌ Django deployment check failed")
            return False
            
    except Exception as e:
        print(f"❌ Error running check: {e}")
        return False
    finally:
        print("=" * 70)

def check_secret_key():
    """Verify SECRET_KEY is not the default"""
    print("\n🔐 Checking SECRET_KEY\n")
    print("=" * 70)
    
    # Read settings
    with open('election_cart/settings.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for insecure default
    if 'django-insecure' in content.lower():
        print("⚠️  Default SECRET_KEY found in settings.py")
        print("   Generate new key for production!")
        return False
    else:
        print("✅ SECRET_KEY appears to be customized")
        return True
    
    print("=" * 70)

def check_debug_default():
    """Verify DEBUG defaults to False"""
    print("\n🐛 Checking DEBUG Configuration\n")
    print("=" * 70)
    
    with open('election_cart/settings.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for proper DEBUG configuration
    if "DEBUG = os.getenv('DEBUG', 'False') == 'True'" in content:
        print("✅ DEBUG defaults to False")
        return True
    elif "DEBUG = True" in content:
        print("❌ DEBUG is hardcoded to True")
        return False
    else:
        print("⚠️  DEBUG configuration unclear")
        return False
    
    print("=" * 70)

def check_allowed_hosts():
    """Check ALLOWED_HOSTS configuration"""
    print("\n🌐 Checking ALLOWED_HOSTS\n")
    print("=" * 70)
    
    with open('election_cart/settings.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'ALLOWED_HOSTS' in content:
        print("✅ ALLOWED_HOSTS is configured")
        print("   Remember to set this in production environment!")
        return True
    else:
        print("❌ ALLOWED_HOSTS not found")
        return False
    
    print("=" * 70)

def check_security_middleware():
    """Verify security middleware is enabled"""
    print("\n🛡️  Checking Security Middleware\n")
    print("=" * 70)
    
    with open('election_cart/settings.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = []
    
    # Check for SecurityMiddleware
    if 'SecurityMiddleware' in content:
        print("✅ SecurityMiddleware enabled")
        checks.append(True)
    else:
        print("❌ SecurityMiddleware not found")
        checks.append(False)
    
    # Check for WhiteNoiseMiddleware
    if 'WhiteNoiseMiddleware' in content:
        print("✅ WhiteNoiseMiddleware enabled")
        checks.append(True)
    else:
        print("⚠️  WhiteNoiseMiddleware not found")
        checks.append(False)
    
    print("=" * 70)
    return all(checks)

def check_database_config():
    """Check database configuration"""
    print("\n💾 Checking Database Configuration\n")
    print("=" * 70)
    
    with open('election_cart/settings.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = []
    
    # Check for DATABASE_URL support
    if 'DATABASE_URL' in content:
        print("✅ DATABASE_URL support enabled")
        checks.append(True)
    else:
        print("⚠️  DATABASE_URL support not found")
        checks.append(False)
    
    # Check for connection pooling
    if 'CONN_MAX_AGE' in content:
        print("✅ Connection pooling configured")
        checks.append(True)
    else:
        print("⚠️  Connection pooling not configured")
        checks.append(False)
    
    print("=" * 70)
    return all(checks)

def check_static_files():
    """Check static files configuration"""
    print("\n📦 Checking Static Files\n")
    print("=" * 70)
    
    from pathlib import Path
    
    checks = []
    
    # Check STATIC_ROOT exists
    static_root = Path('staticfiles')
    if static_root.exists():
        file_count = len(list(static_root.rglob('*.*')))
        print(f"✅ STATIC_ROOT exists ({file_count} files)")
        checks.append(True)
    else:
        print("⚠️  STATIC_ROOT not found - run collectstatic")
        checks.append(False)
    
    # Check WhiteNoise storage
    with open('election_cart/settings.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'CompressedManifestStaticFilesStorage' in content or 'CompressedStaticFilesStorage' in content:
        print("✅ WhiteNoise compression enabled")
        checks.append(True)
    else:
        print("⚠️  WhiteNoise compression not configured")
        checks.append(False)
    
    print("=" * 70)
    return all(checks)

def check_environment_variables():
    """Check required environment variables are documented"""
    print("\n🔐 Checking Environment Variables\n")
    print("=" * 70)
    
    from pathlib import Path
    
    checks = []
    
    # Check .env.example exists
    if Path('.env.example').exists():
        print("✅ .env.example exists")
        checks.append(True)
    else:
        print("⚠️  .env.example not found")
        checks.append(False)
    
    # Check .env.production.template exists
    if Path('.env.production.template').exists():
        print("✅ .env.production.template exists")
        checks.append(True)
    else:
        print("⚠️  .env.production.template not found")
        checks.append(False)
    
    # Check .gitignore excludes .env
    if Path('.gitignore').exists():
        with open('.gitignore', 'r') as f:
            gitignore = f.read()
        if '.env' in gitignore:
            print("✅ .env files excluded from git")
            checks.append(True)
        else:
            print("❌ .env files not excluded from git")
            checks.append(False)
    
    print("=" * 70)
    return all(checks)

def check_deployment_files():
    """Check deployment configuration files"""
    print("\n🚀 Checking Deployment Files\n")
    print("=" * 70)
    
    from pathlib import Path
    
    checks = []
    
    files = {
        'Procfile': 'Railway/Heroku deployment',
        'requirements.txt': 'Python dependencies',
        'runtime.txt': 'Python version',
        'railway.json': 'Railway configuration',
    }
    
    for file, description in files.items():
        if Path(file).exists():
            print(f"✅ {file} exists ({description})")
            checks.append(True)
        else:
            print(f"⚠️  {file} not found ({description})")
            checks.append(False)
    
    print("=" * 70)
    return all(checks)

def security_checklist():
    """Display security checklist"""
    print("\n📋 Pre-Deployment Security Checklist\n")
    print("=" * 70)
    
    checklist = [
        "Generate new DJANGO_SECRET_KEY for production",
        "Set DEBUG=False in production",
        "Configure ALLOWED_HOSTS with your domain",
        "Use DATABASE_URL from Railway",
        "Switch to live Razorpay keys",
        "Configure SENTRY_DSN for error tracking",
        "Update CORS_ALLOWED_ORIGINS with frontend URL",
        "Verify all secrets are in environment variables",
        "Run collectstatic before deployment",
        "Test health endpoint after deployment",
    ]
    
    for item in checklist:
        print(f"  ☐ {item}")
    
    print("=" * 70)

if __name__ == '__main__':
    print("\n🔒 Security and Deployment Checks\n")
    print("=" * 70)
    print("Running comprehensive checks before deployment...")
    print("=" * 70)
    
    try:
        # Run all checks
        results = {
            'Django Check': run_django_check(),
            'SECRET_KEY': check_secret_key(),
            'DEBUG Config': check_debug_default(),
            'ALLOWED_HOSTS': check_allowed_hosts(),
            'Security Middleware': check_security_middleware(),
            'Database Config': check_database_config(),
            'Static Files': check_static_files(),
            'Environment Variables': check_environment_variables(),
            'Deployment Files': check_deployment_files(),
        }
        
        # Display checklist
        security_checklist()
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 Check Summary")
        print("=" * 70)
        
        for check, passed in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"  {check:25} {status}")
        
        print("=" * 70)
        
        passed_count = sum(results.values())
        total_count = len(results)
        
        print(f"\n✅ Passed: {passed_count}/{total_count}")
        
        if all(results.values()):
            print("\n🎉 All checks passed! Ready for deployment!")
            print("\n📝 Next Steps:")
            print("   1. Review the security checklist above")
            print("   2. Set environment variables in Railway")
            print("   3. Deploy using: railway up")
            print("   4. Test health endpoint")
            print("   5. Set up uptime monitoring")
            sys.exit(0)
        else:
            print("\n⚠️  Some checks failed. Review and fix before deploying.")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ Error during checks: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

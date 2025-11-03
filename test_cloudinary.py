"""
Test script to verify Cloudinary configuration
Run with: python test_cloudinary.py
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'election_cart.settings')
django.setup()

from django.conf import settings

print("=" * 80)
print("CLOUDINARY CONFIGURATION TEST")
print("=" * 80)

# Check environment variables
print("\n1. Environment Variables:")
print(f"   CLOUDINARY_CLOUD_NAME: {os.getenv('CLOUDINARY_CLOUD_NAME', 'NOT SET')}")
print(f"   CLOUDINARY_API_KEY: {os.getenv('CLOUDINARY_API_KEY', 'NOT SET')}")
print(f"   CLOUDINARY_API_SECRET: {'SET' if os.getenv('CLOUDINARY_API_SECRET') else 'NOT SET'}")

# Check settings
print("\n2. Django Settings:")
print(f"   USE_CLOUDINARY: {settings.USE_CLOUDINARY}")
print(f"   DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
print(f"   CLOUDINARY_STORAGE: {settings.CLOUDINARY_STORAGE}")

# Check if cloudinary is installed
print("\n3. Package Installation:")
try:
    import cloudinary
    print(f"   ✓ cloudinary package installed")
except ImportError as e:
    print(f"   ✗ cloudinary package NOT installed: {e}")
    print("   → Run: pip install cloudinary")

try:
    import cloudinary_storage
    print(f"   ✓ django-cloudinary-storage package installed")
except ImportError as e:
    print(f"   ✗ django-cloudinary-storage package NOT installed: {e}")
    print("   → Run: pip install django-cloudinary-storage")

# Test Cloudinary connection
print("\n4. Cloudinary Connection Test:")
if settings.USE_CLOUDINARY:
    try:
        import cloudinary
        import cloudinary.api
        
        # Test API connection
        result = cloudinary.api.ping()
        print(f"   ✓ Successfully connected to Cloudinary!")
        print(f"   Response: {result}")
        
        # Get account usage
        try:
            usage = cloudinary.api.usage()
            print(f"\n5. Account Usage:")
            print(f"   Storage: {usage.get('storage', {}).get('usage', 0) / (1024*1024):.2f} MB")
            print(f"   Bandwidth: {usage.get('bandwidth', {}).get('usage', 0) / (1024*1024):.2f} MB")
            print(f"   Transformations: {usage.get('transformations', {}).get('usage', 0)}")
        except Exception as e:
            print(f"   ⚠ Could not get usage info: {e}")
        
    except Exception as e:
        print(f"   ✗ Failed to connect to Cloudinary: {e}")
        print(f"   → Check your credentials in .env file")
else:
    print("   ⚠ Cloudinary is not enabled (USE_CLOUDINARY=False)")
    print("   → Check that all credentials are set in .env file")

# Test image upload
print("\n6. Test Image Upload:")
if settings.USE_CLOUDINARY:
    try:
        import cloudinary.uploader
        from io import BytesIO
        from PIL import Image
        
        # Create a test image
        img = Image.new('RGB', (100, 100), color='red')
        img_bytes = BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            img_bytes,
            folder='test',
            public_id='test_image'
        )
        
        print(f"   ✓ Test image uploaded successfully!")
        print(f"   URL: {result['secure_url']}")
        print(f"   Public ID: {result['public_id']}")
        
        # Clean up test image
        cloudinary.uploader.destroy(result['public_id'])
        print(f"   ✓ Test image deleted")
        
    except Exception as e:
        print(f"   ✗ Failed to upload test image: {e}")
        import traceback
        traceback.print_exc()
else:
    print("   ⚠ Skipped (Cloudinary not enabled)")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)

# Summary
print("\n📋 SUMMARY:")
if settings.USE_CLOUDINARY:
    print("✓ Cloudinary is ENABLED and configured")
    print("✓ Ready to use for image uploads")
else:
    print("✗ Cloudinary is NOT enabled")
    print("→ Check your .env file and ensure all credentials are set")
    print("→ Restart Django server after updating .env")

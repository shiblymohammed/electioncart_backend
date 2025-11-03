"""
Test image upload through API endpoint
Run with: python test_api_upload.py
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'election_cart.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from products.models import Package
from PIL import Image
from io import BytesIO

print("=" * 80)
print("TEST IMAGE UPLOAD THROUGH API")
print("=" * 80)

# Get existing admin user
User = get_user_model()
admin_user = User.objects.filter(is_staff=True, is_superuser=True).first()
if not admin_user:
    print("ERROR: No admin user found. Please create an admin user first.")
    sys.exit(1)
print(f"\n1. Using admin user: {admin_user.email}")

# Get or create test package
package, created = Package.objects.get_or_create(
    name='Test Package API',
    defaults={
        'price': 100.00,
        'description': 'Test package for API upload',
        'features': ['Feature 1'],
        'deliverables': ['Deliverable 1']
    }
)
print(f"2. Using package: {package.name} (ID: {package.id})")

# Create test image
print("\n3. Creating test image...")
img = Image.new('RGB', (800, 600), color='green')
img_bytes = BytesIO()
img.save(img_bytes, format='JPEG')
img_bytes.seek(0)

# Create client and login
client = Client()
client.force_login(admin_user)
print("4. Logged in as admin")

# Upload image through API
print("\n5. Uploading image through API...")
url = f'/api/admin/products/package/{package.id}/images/'
print(f"   URL: {url}")

response = client.post(
    url,
    {
        'image': img_bytes,
        'alt_text': 'Test image via API',
        'is_primary': True
    },
    format='multipart'
)

print(f"\n6. Response:")
print(f"   Status Code: {response.status_code}")
print(f"   Content: {response.content.decode()}")

if response.status_code == 201:
    print("\n" + "=" * 80)
    print("✓ TEST PASSED - API upload works!")
    print("=" * 80)
    
    # Clean up
    import json
    data = json.loads(response.content)
    image_id = data.get('id')
    if image_id:
        from products.models import ProductImage
        ProductImage.objects.filter(id=image_id).delete()
        print("✓ Test image deleted")
else:
    print("\n" + "=" * 80)
    print("✗ TEST FAILED - API upload failed")
    print("=" * 80)

# Clean up
if package.name == 'Test Package API':
    package.delete()
    print("✓ Test package deleted")

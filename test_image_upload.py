"""
Test image upload through Django model
Run with: python test_image_upload.py
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'election_cart.settings')
django.setup()

from django.core.files.uploadedfile import SimpleUploadedFile
from products.models import ProductImage, Package
from django.contrib.contenttypes.models import ContentType
from PIL import Image
from io import BytesIO

print("=" * 80)
print("TEST IMAGE UPLOAD THROUGH DJANGO MODEL")
print("=" * 80)

# Get or create a test package
package, created = Package.objects.get_or_create(
    name='Test Package',
    defaults={
        'price': 100.00,
        'description': 'Test package for image upload',
        'features': ['Feature 1'],
        'deliverables': ['Deliverable 1']
    }
)
print(f"\n1. Using package: {package.name} (ID: {package.id})")

# Create a test image
print("\n2. Creating test image...")
img = Image.new('RGB', (800, 600), color='blue')
img_bytes = BytesIO()
img.save(img_bytes, format='JPEG')
img_bytes.seek(0)

# Create Django file
image_file = SimpleUploadedFile(
    'test_image.jpg',
    img_bytes.read(),
    content_type='image/jpeg'
)

print(f"   ✓ Test image created (size: {len(image_file.read())} bytes)")
image_file.seek(0)

# Upload through Django model
print("\n3. Uploading through ProductImage model...")
try:
    content_type = ContentType.objects.get_for_model(Package)
    
    product_image = ProductImage.objects.create(
        content_type=content_type,
        object_id=package.id,
        image=image_file,
        is_primary=True,
        alt_text='Test image'
    )
    
    print(f"   ✓ Image uploaded successfully!")
    print(f"   Image ID: {product_image.id}")
    print(f"   Image URL: {product_image.image.url}")
    print(f"   Image name: {product_image.image.name}")
    
    # Test serializer
    print("\n4. Testing serializer...")
    from products.serializers import ProductImageSerializer
    from rest_framework.request import Request
    from django.test import RequestFactory
    
    factory = RequestFactory()
    request = factory.get('/')
    
    serializer = ProductImageSerializer(product_image, context={'request': request})
    data = serializer.data
    
    print(f"   ✓ Serializer data:")
    print(f"   - image_url: {data.get('image_url')}")
    print(f"   - thumbnail_url: {data.get('thumbnail_url')}")
    
    # Clean up
    print("\n5. Cleaning up...")
    product_image.delete()
    print(f"   ✓ Test image deleted")
    
    if created:
        package.delete()
        print(f"   ✓ Test package deleted")
    
    print("\n" + "=" * 80)
    print("✓ TEST PASSED - Image upload works correctly!")
    print("=" * 80)
    
except Exception as e:
    print(f"\n   ✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("✗ TEST FAILED")
    print("=" * 80)

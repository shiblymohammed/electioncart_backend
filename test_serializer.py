"""
Test ProductImage serializer with Cloudinary
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'election_cart.settings')
django.setup()

from django.core.files.uploadedfile import SimpleUploadedFile
from products.models import ProductImage, Package
from products.serializers import ProductImageSerializer
from django.contrib.contenttypes.models import ContentType
from PIL import Image
from io import BytesIO
from django.test import RequestFactory

print("=" * 80)
print("TEST PRODUCTIMAGE SERIALIZER")
print("=" * 80)

# Get or create test package
package, created = Package.objects.get_or_create(
    name='Test Package Serializer',
    defaults={
        'price': 100.00,
        'description': 'Test',
        'features': ['F1'],
        'deliverables': ['D1']
    }
)
print(f"\n1. Using package: {package.name} (ID: {package.id})")

# Create test image
print("\n2. Creating and uploading test image...")
img = Image.new('RGB', (800, 600), color='red')
img_bytes = BytesIO()
img.save(img_bytes, format='JPEG')
img_bytes.seek(0)

image_file = SimpleUploadedFile('test.jpg', img_bytes.read(), content_type='image/jpeg')

try:
    content_type = ContentType.objects.get_for_model(Package)
    
    product_image = ProductImage.objects.create(
        content_type=content_type,
        object_id=package.id,
        image=image_file,
        is_primary=True,
        alt_text='Test'
    )
    
    print(f"   ✓ Image uploaded (ID: {product_image.id})")
    print(f"   Image URL: {product_image.image.url}")
    print(f"   Image name: {product_image.image.name}")
    
    # Test serializer
    print("\n3. Testing serializer...")
    factory = RequestFactory()
    request = factory.get('/')
    
    serializer = ProductImageSerializer(product_image, context={'request': request})
    
    print("   Serializing...")
    try:
        data = serializer.data
        print(f"   ✓ Serialization successful!")
        print(f"\n4. Serialized data:")
        print(f"   - id: {data.get('id')}")
        print(f"   - image_url: {data.get('image_url')}")
        print(f"   - thumbnail_url: {data.get('thumbnail_url')}")
        print(f"   - is_primary: {data.get('is_primary')}")
        print(f"   - alt_text: {data.get('alt_text')}")
        
        print("\n" + "=" * 80)
        print("✓ TEST PASSED")
        print("=" * 80)
        
    except Exception as e:
        print(f"   ✗ Serialization failed: {e}")
        import traceback
        traceback.print_exc()
        
        print("\n" + "=" * 80)
        print("✗ TEST FAILED - Serialization error")
        print("=" * 80)
    
    # Clean up
    print("\n5. Cleaning up...")
    product_image.delete()
    print("   ✓ Image deleted")
    
    if created:
        package.delete()
        print("   ✓ Package deleted")
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()

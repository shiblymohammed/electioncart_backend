import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'election_cart.settings')
django.setup()

from products.models import ResourceFieldDefinition, Package
from django.contrib.contenttypes.models import ContentType

print("=" * 80)
print("RESOURCE FIELD DEFINITIONS")
print("=" * 80)

# Get all packages
packages = Package.objects.all()

for package in packages:
    print(f"\nPackage: {package.name} (ID: {package.id})")
    
    # Get content type for this package
    content_type = ContentType.objects.get_for_model(Package)
    
    # Get fields for this package
    fields = ResourceFieldDefinition.objects.filter(
        content_type=content_type,
        object_id=package.id
    ).order_by('order')
    
    if fields.exists():
        for field in fields:
            print(f"  - {field.field_name} (Type: {field.field_type}, Required: {field.is_required})")
    else:
        print("  No resource fields defined")

print("\n" + "=" * 80)

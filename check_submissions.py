import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'election_cart.settings')
django.setup()

from orders.models import DynamicResourceSubmission
from products.models import ResourceFieldDefinition

print("=" * 80)
print("ALL DYNAMIC RESOURCE SUBMISSIONS")
print("=" * 80)

subs = DynamicResourceSubmission.objects.all().select_related('field_definition', 'order_item')

if not subs.exists():
    print("No submissions found!")
else:
    for s in subs:
        print(f"\nSubmission ID: {s.id}")
        print(f"  Order Item: {s.order_item.id}")
        print(f"  Field Name: {s.field_definition.field_name}")
        print(f"  Field Type: {s.field_definition.field_type}")
        print(f"  Text Value: {s.text_value}")
        print(f"  Number Value: {s.number_value}")
        print(f"  File Value: {s.file_value}")
        print(f"  Uploaded At: {s.uploaded_at}")

print("\n" + "=" * 80)
print(f"Total Submissions: {subs.count()}")
print("=" * 80)

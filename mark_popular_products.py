"""
Script to mark products as popular
Run with: python mark_popular_products.py
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'election_cart.settings')
django.setup()

from products.models import Package, Campaign

print("=" * 80)
print("MARK PRODUCTS AS POPULAR")
print("=" * 80)

# Get all active products
packages = Package.objects.filter(is_active=True).order_by('-created_at')
campaigns = Campaign.objects.filter(is_active=True).order_by('-created_at')

print(f"\nAvailable Packages ({packages.count()}):")
for idx, pkg in enumerate(packages, 1):
    popular_status = f"[Popular #{pkg.popular_order}]" if pkg.is_popular else ""
    print(f"  {idx}. {pkg.name} - ₹{pkg.price} {popular_status}")

print(f"\nAvailable Campaigns ({campaigns.count()}):")
for idx, cmp in enumerate(campaigns, 1):
    popular_status = f"[Popular #{cmp.popular_order}]" if cmp.is_popular else ""
    print(f"  {idx}. {cmp.name} - ₹{cmp.price}/{cmp.unit} {popular_status}")

print("\n" + "=" * 80)
print("MARKING PRODUCTS AS POPULAR")
print("=" * 80)

# Mark first 3 packages as popular
print("\n1. Marking Packages as Popular...")
popular_packages = packages[:3]
for idx, pkg in enumerate(popular_packages, 1):
    pkg.is_popular = True
    pkg.popular_order = idx
    pkg.save()
    print(f"   ✓ {pkg.name} → Popular #{idx}")

# Mark first 3 campaigns as popular
print("\n2. Marking Campaigns as Popular...")
popular_campaigns = campaigns[:3]
for idx, cmp in enumerate(popular_campaigns, 1):
    cmp.is_popular = True
    cmp.popular_order = idx
    cmp.save()
    print(f"   ✓ {cmp.name} → Popular #{idx}")

print("\n" + "=" * 80)
print("VERIFICATION")
print("=" * 80)

# Verify
popular_pkg_count = Package.objects.filter(is_popular=True).count()
popular_cmp_count = Campaign.objects.filter(is_popular=True).count()

print(f"\n✓ Popular Packages: {popular_pkg_count}/3")
for pkg in Package.objects.filter(is_popular=True).order_by('popular_order'):
    print(f"  #{pkg.popular_order}: {pkg.name}")

print(f"\n✓ Popular Campaigns: {popular_cmp_count}/3")
for cmp in Campaign.objects.filter(is_popular=True).order_by('popular_order'):
    print(f"  #{cmp.popular_order}: {cmp.name}")

print("\n" + "=" * 80)
print("✅ DONE! Products marked as popular")
print("=" * 80)
print("\nNext steps:")
print("1. Visit http://localhost:3000 to see popular products on homepage")
print("2. Test API: curl http://localhost:8000/api/packages/popular/")
print("3. Test API: curl http://localhost:8000/api/campaigns/popular/")

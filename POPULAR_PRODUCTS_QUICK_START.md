# Popular Products - Quick Start Guide

## 🚀 Quick Start (5 Minutes)

### Step 1: Mark Products as Popular (Django Shell)

```bash
python manage.py shell
```

```python
from products.models import Package, Campaign

# Mark 3 packages as popular
packages = Package.objects.filter(is_active=True)[:3]
for idx, pkg in enumerate(packages, 1):
    pkg.is_popular = True
    pkg.popular_order = idx
    pkg.save()
    print(f"✓ {pkg.name} marked as Popular #{idx}")

# Mark 3 campaigns as popular
campaigns = Campaign.objects.filter(is_active=True)[:3]
for idx, cmp in enumerate(campaigns, 1):
    cmp.is_popular = True
    cmp.popular_order = idx
    cmp.save()
    print(f"✓ {cmp.name} marked as Popular #{idx}")

# Verify
print(f"\nPopular Packages: {Package.objects.filter(is_popular=True).count()}")
print(f"Popular Campaigns: {Campaign.objects.filter(is_popular=True).count()}")
```

### Step 2: Test API Endpoints

```bash
# Test popular packages endpoint
curl http://localhost:8000/api/packages/popular/

# Test popular campaigns endpoint
curl http://localhost:8000/api/campaigns/popular/
```

### Step 3: View on Homepage

1. Go to Suburbia homepage: http://localhost:3000
2. Scroll to "Popular Packages" section
3. Scroll to "Popular Campaigns" section
4. You should see the 3 products you marked as popular

---

## 🎯 Admin Usage

### Toggle Popular Status (API)

```bash
# Get admin token first
TOKEN="your_admin_token_here"

# Toggle package popular
curl -X PATCH http://localhost:8000/api/admin/products/packages/1/toggle-popular/ \
  -H "Authorization: Bearer $TOKEN"

# Toggle campaign popular
curl -X PATCH http://localhost:8000/api/admin/products/campaigns/1/toggle-popular/ \
  -H "Authorization: Bearer $TOKEN"
```

### In Admin Frontend (After Integration)

1. Go to Products list
2. Click "Mark as Popular" button on any product
3. Product becomes Popular #1, #2, or #3
4. Click again to unmark
5. Maximum 3 products can be popular at once

---

## 📊 Check Current Popular Products

```bash
python manage.py shell
```

```python
from products.models import Package, Campaign

# List popular packages
print("Popular Packages:")
for pkg in Package.objects.filter(is_popular=True).order_by('popular_order'):
    print(f"  #{pkg.popular_order}: {pkg.name}")

# List popular campaigns
print("\nPopular Campaigns:")
for cmp in Campaign.objects.filter(is_popular=True).order_by('popular_order'):
    print(f"  #{cmp.popular_order}: {cmp.name}")
```

---

## 🔧 Troubleshooting

### Issue: Popular section shows no products

**Solution:**
```python
# Mark some products as popular
from products.models import Package
pkg = Package.objects.first()
pkg.is_popular = True
pkg.popular_order = 1
pkg.save()
```

### Issue: More than 3 products showing

**Solution:**
```python
# Reset popular products
from products.models import Package, Campaign
Package.objects.update(is_popular=False, popular_order=0)
Campaign.objects.update(is_popular=False, popular_order=0)

# Mark only 3
packages = Package.objects.filter(is_active=True)[:3]
for idx, pkg in enumerate(packages, 1):
    pkg.is_popular = True
    pkg.popular_order = idx
    pkg.save()
```

### Issue: Wrong order

**Solution:**
```python
# Reorder popular packages
from products.models import Package
popular = Package.objects.filter(is_popular=True).order_by('id')
for idx, pkg in enumerate(popular, 1):
    pkg.popular_order = idx
    pkg.save()
```

---

## 📝 Quick Commands

```bash
# Check popular count
python manage.py shell -c "from products.models import Package, Campaign; print('Packages:', Package.objects.filter(is_popular=True).count()); print('Campaigns:', Campaign.objects.filter(is_popular=True).count())"

# Reset all popular
python manage.py shell -c "from products.models import Package, Campaign; Package.objects.update(is_popular=False, popular_order=0); Campaign.objects.update(is_popular=False, popular_order=0); print('Reset complete')"

# Mark first 3 as popular
python manage.py shell -c "from products.models import Package; [setattr(pkg, 'is_popular', True) or setattr(pkg, 'popular_order', idx) or pkg.save() for idx, pkg in enumerate(Package.objects.filter(is_active=True)[:3], 1)]; print('Done')"
```

---

## 🎉 That's It!

Your popular products feature is now working. Products marked as popular will automatically appear in the homepage sections.

**Next Steps:**
1. Mark your desired products as popular
2. Integrate PopularToggleButton into admin UI
3. Test the toggle functionality
4. Enjoy! 🚀

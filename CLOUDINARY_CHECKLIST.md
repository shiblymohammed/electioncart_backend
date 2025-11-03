# Cloudinary Setup Checklist

## Quick Setup (5 minutes)

### 1. Install Dependencies ✓
```bash
cd backend
pip install -r requirements.txt
```

### 2. Get Cloudinary Account ✓
- [ ] Go to https://cloudinary.com/users/register_free
- [ ] Sign up (free - 25GB storage, 25GB bandwidth)
- [ ] Copy credentials from Dashboard:
  - Cloud Name: `_______________`
  - API Key: `_______________`
  - API Secret: `_______________`

### 3. Configure Environment ✓
Add to `backend/.env`:
```bash
CLOUDINARY_CLOUD_NAME=your_cloud_name_here
CLOUDINARY_API_KEY=your_api_key_here
CLOUDINARY_API_SECRET=your_api_secret_here
```

### 4. Restart Server ✓
```bash
python manage.py runserver
```

### 5. Test Upload ✓
- [ ] Go to Django admin: http://localhost:8000/admin
- [ ] Navigate to Products → Product Images
- [ ] Upload a test image
- [ ] Check URL - should start with `https://res.cloudinary.com/`

---

## Verification

### Check Configuration
```bash
python manage.py shell
```

```python
from django.conf import settings

# Should print True
print("Cloudinary enabled:", settings.USE_CLOUDINARY)

# Should print your cloud name
print("Cloud name:", settings.CLOUDINARY_STORAGE['CLOUD_NAME'])

# Should print cloudinary storage
print("Storage backend:", settings.DEFAULT_FILE_STORAGE)
```

### Test Upload
```python
from products.models import ProductImage
from django.contrib.contenttypes.models import ContentType
from products.models import Package

# Get a package
package = Package.objects.first()
content_type = ContentType.objects.get_for_model(Package)

# Upload test image
with open('test_image.jpg', 'rb') as f:
    from django.core.files.uploadedfile import SimpleUploadedFile
    image_file = SimpleUploadedFile('test.jpg', f.read(), content_type='image/jpeg')
    
    product_image = ProductImage.objects.create(
        content_type=content_type,
        object_id=package.id,
        image=image_file,
        is_primary=True
    )
    
    print("Image URL:", product_image.image.url)
    # Should be: https://res.cloudinary.com/your_cloud_name/...
```

---

## Migration (Optional)

### Migrate Existing Images
```bash
# Dry run first (see what would be migrated)
python manage.py migrate_to_cloudinary --dry-run

# Actual migration (keeps local files)
python manage.py migrate_to_cloudinary

# Migration with cleanup (deletes local files)
python manage.py migrate_to_cloudinary --delete-local
```

---

## Monitoring

### Cloudinary Dashboard
- [ ] Go to https://cloudinary.com/console
- [ ] Check "Usage" tab
- [ ] Monitor:
  - Storage used: _____ / 25GB
  - Bandwidth used: _____ / 25GB
  - Transformations: _____ / 25,000

---

## Troubleshooting

### ❌ Images not uploading to Cloudinary
**Check**:
- [ ] Environment variables are set correctly
- [ ] Server was restarted after adding env vars
- [ ] `USE_CLOUDINARY=True` in settings

### ❌ Still using local storage
**Check**:
- [ ] Cloudinary credentials are valid
- [ ] No typos in environment variable names
- [ ] `DEFAULT_FILE_STORAGE` points to Cloudinary

### ❌ Cloudinary URLs not working
**Check**:
- [ ] Cloud name is correct
- [ ] Images are public (not private)
- [ ] Check Cloudinary dashboard for errors

---

## Success Criteria

✅ **Setup Complete When**:
- [ ] Dependencies installed
- [ ] Environment variables configured
- [ ] Server restarted
- [ ] Test image uploaded
- [ ] Image URL is Cloudinary URL
- [ ] Image loads correctly in browser

✅ **Production Ready When**:
- [ ] All existing images migrated (optional)
- [ ] Frontend tested with Cloudinary images
- [ ] Performance improvements verified
- [ ] Monitoring set up in Cloudinary dashboard

---

## Quick Reference

### Get Optimized URL (Python)
```python
from products.cloudinary_utils import CloudinaryHelper

url = CloudinaryHelper.get_thumbnail_url('image_id', size=300)
```

### Get Optimized URL (JavaScript)
```javascript
// Already optimized - no changes needed!
const imageUrl = product.primary_image.image_url;
```

### Manual Transformation (URL)
```
Original:
https://res.cloudinary.com/demo/image/upload/v1234/sample.jpg

Thumbnail:
https://res.cloudinary.com/demo/image/upload/w_300,h_300,c_fill/v1234/sample.jpg

Optimized:
https://res.cloudinary.com/demo/image/upload/w_800,q_auto,f_auto/v1234/sample.jpg
```

---

## Documentation

- **Setup Guide**: `CLOUDINARY_SETUP_STEPS.md`
- **Quick Reference**: `CLOUDINARY_QUICK_REFERENCE.md`
- **Full Implementation**: `CLOUDINARY_IMPLEMENTATION.md`
- **Summary**: `CLOUDINARY_IMPLEMENTATION_SUMMARY.md`

---

## Support

- Cloudinary Docs: https://cloudinary.com/documentation
- Django Integration: https://cloudinary.com/documentation/django_integration
- Support: https://support.cloudinary.com

---

## Status

- [x] Implementation complete
- [ ] Dependencies installed
- [ ] Environment configured
- [ ] Server restarted
- [ ] Upload tested
- [ ] Migration complete (optional)
- [ ] Production deployed

---

**Last Updated**: November 3, 2025
**Status**: Ready for setup ✅

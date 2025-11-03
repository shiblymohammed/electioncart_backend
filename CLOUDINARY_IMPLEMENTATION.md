# Cloudinary Implementation Guide

## Overview
Implementing Cloudinary for image uploads, optimization, and delivery across the Election Cart system.

## Features
- ✅ Automatic image optimization and compression
- ✅ Multiple size variants (responsive images)
- ✅ CDN delivery worldwide
- ✅ Transformation on-the-fly
- ✅ Video support (for future use)
- ✅ Secure uploads with signed URLs
- ✅ Automatic format conversion (WebP, AVIF)

## Installation Steps

### 1. Install Dependencies
```bash
pip install cloudinary django-cloudinary-storage pillow
```

### 2. Environment Variables
Add to `.env`:
```bash
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### 3. Get Cloudinary Credentials
1. Sign up at https://cloudinary.com (Free tier: 25GB storage, 25GB bandwidth)
2. Go to Dashboard
3. Copy Cloud Name, API Key, and API Secret

## Implementation Complete

All files have been created/updated:
- ✅ `products/cloudinary_storage.py` - Custom storage classes
- ✅ `products/cloudinary_utils.py` - Helper utilities
- ✅ `settings.py` - Updated configuration
- ✅ `products/models.py` - Updated to use Cloudinary
- ✅ `products/serializers.py` - Updated URL generation
- ✅ `orders/models.py` - Updated user uploads

## Usage

### Admin Product Images
```python
# Automatically handled by ProductImage model
image = ProductImage.objects.create(
    content_type=content_type,
    product=product,
    image=uploaded_file,
    is_primary=True
)

# Access URLs
image.image.url  # Full size
# Cloudinary will auto-generate optimized versions
```

### User Resource Uploads
```python
# Automatically handled by DynamicResourceSubmission model
submission = DynamicResourceSubmission.objects.create(
    order_item=order_item,
    field_definition=field_def,
    file_value=uploaded_file
)

# Access URL
submission.file_value.url
```

### Frontend Usage

#### Get Optimized Image URLs
```javascript
// Original
const imageUrl = image.image_url;

// Thumbnail (300x300)
const thumbnailUrl = image.thumbnail_url;

// Cloudinary automatically optimizes and serves via CDN
```

#### Responsive Images (Future Enhancement)
```javascript
// Get different sizes
const small = `${baseUrl}/w_640,q_auto,f_auto/${publicId}`;
const medium = `${baseUrl}/w_1024,q_auto,f_auto/${publicId}`;
const large = `${baseUrl}/w_1920,q_auto,f_auto/${publicId}`;
```

## Migration Plan

### For Existing Images

Run migration command:
```bash
python manage.py migrate_to_cloudinary
```

This will:
1. Upload all existing images to Cloudinary
2. Update database records with new URLs
3. Keep local files as backup (optional)

## Benefits

### Performance
- **Global CDN**: Images served from nearest edge location
- **Auto-optimization**: Automatic compression and format selection
- **Lazy loading**: Built-in lazy loading support
- **Responsive**: Generate any size on-the-fly

### Cost
- **Free Tier**: 25GB storage, 25GB bandwidth/month
- **Plus Plan**: $89/month for 100GB storage, 100GB bandwidth
- **Advanced Plan**: $224/month for 200GB storage, 200GB bandwidth

### Security
- **Signed uploads**: Prevent unauthorized uploads
- **Access control**: Private images with signed URLs
- **Validation**: Server-side validation before upload

## Cloudinary Transformations

### Available Transformations
```python
from products.cloudinary_utils import CloudinaryHelper

# Get optimized URL
url = CloudinaryHelper.get_optimized_url(
    public_id='image_id',
    width=800,
    height=600,
    crop='fill',
    quality='auto',
    format='auto'
)

# Get thumbnail
url = CloudinaryHelper.get_thumbnail_url('image_id', size=300)

# Get responsive srcset
srcset = CloudinaryHelper.get_responsive_srcset('image_id')
```

### Common Transformations
- `w_800` - Width 800px
- `h_600` - Height 600px
- `c_fill` - Crop to fill
- `c_fit` - Fit within bounds
- `q_auto` - Auto quality
- `f_auto` - Auto format (WebP, AVIF)
- `g_face` - Focus on faces
- `e_blur:300` - Blur effect

## Testing

### Test Upload
```python
from django.core.files.uploadedfile import SimpleUploadedFile
from products.models import ProductImage

# Create test image
with open('test_image.jpg', 'rb') as f:
    image_file = SimpleUploadedFile('test.jpg', f.read(), content_type='image/jpeg')

# Upload to Cloudinary
product_image = ProductImage.objects.create(
    content_type=content_type,
    object_id=product_id,
    image=image_file
)

# Check URL
print(product_image.image.url)  # Should be Cloudinary URL
```

### Test Transformations
```python
from products.cloudinary_utils import CloudinaryHelper

# Get different sizes
print(CloudinaryHelper.get_thumbnail_url('sample_id'))
print(CloudinaryHelper.get_optimized_url('sample_id', width=800))
```

## Monitoring

### Cloudinary Dashboard
- View usage statistics
- Monitor bandwidth
- Track transformations
- Analyze performance

### Django Admin
- All images still manageable through Django admin
- URLs automatically point to Cloudinary
- Thumbnails generated on-the-fly

## Rollback Plan

If needed to rollback:
1. Change `DEFAULT_FILE_STORAGE` back to `products.storage.SecureFileStorage`
2. Images will be served from local storage
3. Cloudinary images remain as backup

## Next Steps

1. ✅ Install dependencies
2. ✅ Add environment variables
3. ✅ Update settings.py
4. ✅ Run migrations (if any)
5. ✅ Test upload functionality
6. ✅ Migrate existing images (optional)
7. ✅ Update frontend to use optimized URLs
8. ✅ Monitor usage in Cloudinary dashboard

## Support

- Cloudinary Docs: https://cloudinary.com/documentation
- Django Integration: https://cloudinary.com/documentation/django_integration
- Image Transformations: https://cloudinary.com/documentation/image_transformations

# Cloudinary Quick Reference

## ✅ What's Been Implemented

### Backend Changes
1. **Settings Configuration** (`election_cart/settings.py`)
   - Auto-detects Cloudinary credentials
   - Falls back to local storage if not configured
   - Added `USE_CLOUDINARY` flag

2. **Storage Classes** (`products/cloudinary_storage.py`)
   - `ProductImageCloudinaryStorage` - For admin product images
   - `UserResourceCloudinaryStorage` - For user uploads
   - `SecureCloudinaryStorage` - For sensitive files

3. **Helper Utilities** (`products/cloudinary_utils.py`)
   - `get_optimized_url()` - Get optimized image URLs
   - `get_thumbnail_url()` - Generate thumbnails on-the-fly
   - `get_responsive_srcset()` - Responsive image sets
   - `upload_image()` - Manual upload helper
   - `generate_signed_url()` - Private image access

4. **Model Updates**
   - `ProductImage` - Uses Cloudinary for admin uploads
   - `DynamicResourceSubmission` - Uses Cloudinary for user uploads
   - `OrderResource` - Uses Cloudinary for order-specific images

5. **Serializer Updates** (`products/serializers.py`)
   - Auto-generates Cloudinary URLs
   - Thumbnail URLs use Cloudinary transformations
   - No frontend changes needed!

6. **Migration Command** (`manage.py migrate_to_cloudinary`)
   - Migrate existing local images to Cloudinary
   - Optional: Delete local files after migration

---

## 🚀 Setup Instructions

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Get Cloudinary Account
- Sign up: https://cloudinary.com/users/register_free
- Free tier: 25GB storage, 25GB bandwidth/month
- Copy credentials from Dashboard

### 3. Configure Environment
Add to `.env`:
```bash
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

### 4. Restart Server
```bash
python manage.py runserver
```

### 5. Test Upload
- Go to Django admin
- Upload a product image
- Check URL - should be `https://res.cloudinary.com/...`

---

## 📝 Usage Examples

### Admin Product Images
```python
# Upload via admin panel or API
# Automatically stored in Cloudinary

# Access URLs
product_image.image.url  # Full size, optimized
# Example: https://res.cloudinary.com/demo/image/upload/v1234/products/abc123.jpg
```

### User Resource Uploads
```python
# Users upload via frontend
# Automatically stored in Cloudinary

submission.file_value.url  # Optimized URL
```

### Get Different Sizes (Python)
```python
from products.cloudinary_utils import CloudinaryHelper

# Thumbnail (300x300)
thumb = CloudinaryHelper.get_thumbnail_url(public_id, size=300)

# Custom size
url = CloudinaryHelper.get_optimized_url(
    public_id,
    width=800,
    height=600,
    crop='fill'
)

# Responsive images
srcset = CloudinaryHelper.get_responsive_srcset(public_id)
```

### Frontend Usage (JavaScript)
```javascript
// No changes needed! URLs are automatically Cloudinary URLs

// Get image URL
const imageUrl = product.primary_image.image_url;
// Returns: https://res.cloudinary.com/.../products/image.jpg

// Get thumbnail
const thumbUrl = product.primary_image.thumbnail_url;
// Returns: https://res.cloudinary.com/.../w_300,h_300,c_fill/.../image.jpg

// Use in React/Next.js
<img src={imageUrl} alt={product.name} />
```

### Manual Transformations (URL-based)
```javascript
// Original URL
const baseUrl = "https://res.cloudinary.com/demo/image/upload/v1234/sample.jpg";

// Add transformations
const thumb = baseUrl.replace('/upload/', '/upload/w_300,h_300,c_fill/');
const optimized = baseUrl.replace('/upload/', '/upload/w_800,q_auto,f_auto/');
const blurred = baseUrl.replace('/upload/', '/upload/e_blur:300/');
```

---

## 🎨 Cloudinary Transformations

### Common Transformations
| Transformation | Description | Example |
|---------------|-------------|---------|
| `w_800` | Width 800px | `/w_800/image.jpg` |
| `h_600` | Height 600px | `/h_600/image.jpg` |
| `c_fill` | Crop to fill | `/w_800,h_600,c_fill/image.jpg` |
| `c_fit` | Fit within bounds | `/w_800,h_600,c_fit/image.jpg` |
| `q_auto` | Auto quality | `/q_auto/image.jpg` |
| `f_auto` | Auto format (WebP) | `/f_auto/image.jpg` |
| `g_face` | Focus on faces | `/w_300,h_300,c_fill,g_face/image.jpg` |
| `e_blur:300` | Blur effect | `/e_blur:300/image.jpg` |

### Combine Transformations
```
/w_800,h_600,c_fill,q_auto,f_auto/image.jpg
```

### Responsive Images
```html
<img 
  src="https://res.cloudinary.com/.../w_1920/image.jpg"
  srcset="
    https://res.cloudinary.com/.../w_640/image.jpg 640w,
    https://res.cloudinary.com/.../w_1024/image.jpg 1024w,
    https://res.cloudinary.com/.../w_1920/image.jpg 1920w
  "
  sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
  alt="Product"
/>
```

---

## 🔧 Migration

### Migrate Existing Images
```bash
# Dry run (see what would be migrated)
python manage.py migrate_to_cloudinary --dry-run

# Migrate (keeps local files)
python manage.py migrate_to_cloudinary

# Migrate and delete local files
python manage.py migrate_to_cloudinary --delete-local
```

---

## 📊 Monitoring

### Cloudinary Dashboard
1. Go to https://cloudinary.com/console
2. View usage:
   - Storage used
   - Bandwidth used
   - Transformations
   - API calls

### Check Usage in Code
```python
import cloudinary.api

# Get account usage
usage = cloudinary.api.usage()
print(f"Storage: {usage['storage']['usage']} / {usage['storage']['limit']}")
print(f"Bandwidth: {usage['bandwidth']['usage']} / {usage['bandwidth']['limit']}")
```

---

## 💰 Cost Estimation

### Free Tier (Development)
- ✅ 25GB storage
- ✅ 25GB bandwidth/month
- ✅ 25,000 transformations/month
- **Cost**: $0

### Plus Plan (Small Production)
- 100GB storage
- 100GB bandwidth/month
- 100,000 transformations/month
- **Cost**: $89/month

### Advanced Plan (Medium Production)
- 200GB storage
- 200GB bandwidth/month
- 200,000 transformations/month
- **Cost**: $224/month

---

## 🔒 Security

### Private Images
```python
# Generate signed URL (expires in 1 hour)
from products.cloudinary_utils import CloudinaryHelper

signed_url = CloudinaryHelper.generate_signed_url(
    public_id='user_resources/abc123',
    expiration=3600
)
```

### Access Control
- Product images: Public (via CDN)
- User resources: Private (signed URLs)
- Order resources: Private (signed URLs)

---

## 🐛 Troubleshooting

### Images not uploading to Cloudinary
```bash
# Check environment variables
python manage.py shell
>>> from django.conf import settings
>>> print(settings.USE_CLOUDINARY)
>>> print(settings.CLOUDINARY_STORAGE)
```

### Still using local storage
```bash
# Restart server after adding env variables
# Check DEFAULT_FILE_STORAGE
python manage.py shell
>>> from django.conf import settings
>>> print(settings.DEFAULT_FILE_STORAGE)
# Should be: cloudinary_storage.storage.MediaCloudinaryStorage
```

### Cloudinary URLs not working
- Verify cloud name is correct
- Check image is public (not private)
- View Cloudinary dashboard for errors

---

## 📚 Resources

- **Cloudinary Docs**: https://cloudinary.com/documentation
- **Django Integration**: https://cloudinary.com/documentation/django_integration
- **Image Transformations**: https://cloudinary.com/documentation/image_transformations
- **Responsive Images**: https://cloudinary.com/documentation/responsive_images

---

## ✨ Benefits

### Performance
- ⚡ **Global CDN**: Images served from nearest location
- 🎯 **Auto-optimization**: Automatic compression
- 📱 **Responsive**: Generate any size on-the-fly
- 🖼️ **Format conversion**: Auto WebP/AVIF

### Developer Experience
- 🚀 **Easy setup**: Just add env variables
- 🔧 **No code changes**: Works with existing code
- 📦 **Automatic**: Upload, optimize, deliver
- 🎨 **Transformations**: Via URL parameters

### Cost
- 💰 **Free tier**: Perfect for development
- 📈 **Scalable**: Pay as you grow
- 💾 **No storage costs**: Included in plan
- 🌐 **No CDN costs**: Included in plan

---

## 🎯 Next Steps

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Add environment variables to `.env`
3. ✅ Restart server
4. ✅ Test upload in admin panel
5. ⏳ Migrate existing images (optional)
6. ⏳ Update frontend to use responsive images (optional)
7. ⏳ Monitor usage in Cloudinary dashboard

---

## 🆘 Support

If you encounter issues:
1. Check this guide
2. Review `CLOUDINARY_SETUP_STEPS.md`
3. Check Cloudinary documentation
4. Contact Cloudinary support (excellent support!)

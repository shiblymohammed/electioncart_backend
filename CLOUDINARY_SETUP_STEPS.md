# Cloudinary Setup - Quick Start Guide

## Step 1: Install Dependencies

```bash
cd backend
pip install cloudinary django-cloudinary-storage
```

Or install from requirements.txt:
```bash
pip install -r requirements.txt
```

## Step 2: Get Cloudinary Credentials

1. Go to https://cloudinary.com/users/register_free
2. Sign up for a free account (25GB storage, 25GB bandwidth/month)
3. After login, go to Dashboard
4. Copy these values:
   - Cloud Name
   - API Key
   - API Secret

## Step 3: Configure Environment Variables

Add to your `.env` file:

```bash
# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name_here
CLOUDINARY_API_KEY=your_api_key_here
CLOUDINARY_API_SECRET=your_api_secret_here
```

## Step 4: Test the Setup

```bash
python manage.py shell
```

Then run:
```python
from django.conf import settings
print("Cloudinary enabled:", settings.USE_CLOUDINARY)
print("Cloud name:", settings.CLOUDINARY_STORAGE['CLOUD_NAME'])

# Test upload
import cloudinary
import cloudinary.uploader
result = cloudinary.uploader.upload("test_image.jpg")
print("Upload successful:", result['secure_url'])
```

## Step 5: Verify in Django Admin

1. Start server: `python manage.py runserver`
2. Go to admin panel
3. Upload a product image
4. Check the image URL - it should be a Cloudinary URL like:
   `https://res.cloudinary.com/your_cloud_name/image/upload/...`

## Features Now Available

✅ **Automatic Optimization**: Images automatically compressed
✅ **CDN Delivery**: Served from nearest edge location globally
✅ **Responsive Images**: Generate any size on-the-fly
✅ **Format Conversion**: Auto WebP/AVIF for modern browsers
✅ **Transformations**: Resize, crop, blur, etc. via URL
✅ **Secure Storage**: Private images with signed URLs

## Usage Examples

### Get Optimized Image URL
```python
from products.cloudinary_utils import CloudinaryHelper

# Get thumbnail (300x300)
url = CloudinaryHelper.get_thumbnail_url('image_public_id', size=300)

# Get optimized URL with custom size
url = CloudinaryHelper.get_optimized_url(
    'image_public_id',
    width=800,
    height=600,
    crop='fill'
)

# Get responsive srcset
srcset = CloudinaryHelper.get_responsive_srcset('image_public_id')
```

### Frontend Usage
```javascript
// Image URLs are automatically Cloudinary URLs
const imageUrl = product.primary_image.image_url;
const thumbnailUrl = product.primary_image.thumbnail_url;

// Both are optimized and served via CDN
```

## Monitoring Usage

1. Go to Cloudinary Dashboard
2. View "Usage" tab
3. Monitor:
   - Storage used
   - Bandwidth used
   - Transformations
   - API calls

## Troubleshooting

### Images not uploading to Cloudinary
- Check environment variables are set correctly
- Verify `USE_CLOUDINARY=True` in settings
- Check Cloudinary credentials are valid

### Images still using local storage
- Restart Django server after adding env variables
- Check `DEFAULT_FILE_STORAGE` in settings
- Verify Cloudinary is installed: `pip list | grep cloudinary`

### Cloudinary URLs not working
- Check if cloud name is correct
- Verify images are public (not private)
- Check Cloudinary dashboard for upload errors

## Cost Estimation

### Free Tier (Perfect for Development)
- 25GB storage
- 25GB bandwidth/month
- 25,000 transformations/month
- **Cost**: $0

### Plus Plan (Good for Small Production)
- 100GB storage
- 100GB bandwidth/month
- 100,000 transformations/month
- **Cost**: $89/month

### Advanced Plan (Medium Production)
- 200GB storage
- 200GB bandwidth/month
- 200,000 transformations/month
- **Cost**: $224/month

## Next Steps

1. ✅ Install dependencies
2. ✅ Add environment variables
3. ✅ Test upload
4. ⏳ Migrate existing images (optional)
5. ⏳ Update frontend to use optimized URLs
6. ⏳ Monitor usage

## Migration Command (Optional)

To migrate existing local images to Cloudinary:

```bash
python manage.py migrate_to_cloudinary
```

This will:
- Upload all existing images to Cloudinary
- Update database records
- Keep local files as backup

# Production Image Handling Recommendations

## Current Status vs Production Requirements

### ✅ Already Implemented (Good for Production)
1. **Secure Storage** - Files outside web root with proper permissions
2. **File Validation** - MIME type checking, size limits, extension validation
3. **Authentication** - JWT-based access control
4. **Authorization** - Owner/staff/admin checks
5. **Secure Naming** - UUID-based filenames prevent guessing
6. **Organized Structure** - Date-based folder organization

### 🔧 Critical Production Improvements Needed

## 1. CDN Integration for Image Delivery

### Why?
- **Performance**: Faster image loading globally
- **Bandwidth**: Reduce server load
- **Scalability**: Handle traffic spikes
- **Caching**: Browser and edge caching

### Implementation Options:

#### Option A: AWS CloudFront + S3
```python
# settings.py
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'ap-south-1')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_CLOUDFRONT_DOMAIN = os.getenv('AWS_CLOUDFRONT_DOMAIN')

# Use CloudFront for public product images
CDN_BASE_URL = f'https://{AWS_CLOUDFRONT_DOMAIN}/'

# Separate storage for public vs private files
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
PRIVATE_FILE_STORAGE = 'products.storage.PrivateS3Storage'
```

```python
# products/storage.py - Add S3 storage classes
from storages.backends.s3boto3 import S3Boto3Storage

class PublicMediaStorage(S3Boto3Storage):
    """Public S3 storage for product images (served via CloudFront)"""
    location = 'media/public'
    default_acl = 'public-read'
    file_overwrite = False
    custom_domain = settings.AWS_CLOUDFRONT_DOMAIN

class PrivateMediaStorage(S3Boto3Storage):
    """Private S3 storage for user uploads (served via signed URLs)"""
    location = 'media/private'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = None  # Don't use CloudFront for private files
```

#### Option B: Cloudinary (Easier Setup)
```python
# settings.py
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET')
}

# Use Cloudinary for product images
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
```

**Recommendation**: Use **AWS S3 + CloudFront** for better control and cost-effectiveness at scale.

---

## 2. Image Optimization Pipeline

### Current Issue:
- Images uploaded at full resolution
- No automatic compression
- No responsive image variants

### Solution: Implement Image Processing

```python
# products/image_processor.py
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

class ImageProcessor:
    """Process and optimize images for production"""
    
    SIZES = {
        'thumbnail': (300, 300),
        'small': (640, 640),
        'medium': (1024, 1024),
        'large': (1920, 1920),
    }
    
    @staticmethod
    def create_variants(image_file):
        """Create multiple size variants of an image"""
        img = Image.open(image_file)
        
        # Convert to RGB if necessary
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        
        variants = {}
        
        for size_name, dimensions in ImageProcessor.SIZES.items():
            # Create a copy
            img_copy = img.copy()
            
            # Resize maintaining aspect ratio
            img_copy.thumbnail(dimensions, Image.Resampling.LANCZOS)
            
            # Save to BytesIO
            output = BytesIO()
            
            # Use WebP for better compression (fallback to JPEG)
            try:
                img_copy.save(output, format='WEBP', quality=85, optimize=True)
                ext = '.webp'
            except:
                img_copy.save(output, format='JPEG', quality=85, optimize=True)
                ext = '.jpg'
            
            output.seek(0)
            
            # Create file
            variants[size_name] = InMemoryUploadedFile(
                output,
                None,
                f'{size_name}{ext}',
                f'image/{"webp" if ext == ".webp" else "jpeg"}',
                sys.getsizeof(output),
                None
            )
        
        return variants
    
    @staticmethod
    def optimize_image(image_file, max_width=1920, quality=85):
        """Optimize a single image"""
        img = Image.open(image_file)
        
        # Convert to RGB
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        
        # Resize if too large
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
        # Save optimized
        output = BytesIO()
        img.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)
        
        return InMemoryUploadedFile(
            output,
            None,
            'optimized.jpg',
            'image/jpeg',
            sys.getsizeof(output),
            None
        )
```

```python
# products/models.py - Update ProductImage model
class ProductImage(models.Model):
    # ... existing fields ...
    
    # Add image variants
    image_small = models.ImageField(upload_to='product_images/small/', blank=True, null=True)
    image_medium = models.ImageField(upload_to='product_images/medium/', blank=True, null=True)
    image_large = models.ImageField(upload_to='product_images/large/', blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.image and not self.pk:  # New upload
            from .image_processor import ImageProcessor
            
            # Create variants
            variants = ImageProcessor.create_variants(self.image)
            
            self.thumbnail = variants['thumbnail']
            self.image_small = variants['small']
            self.image_medium = variants['medium']
            self.image_large = variants['large']
        
        super().save(*args, **kwargs)
```

---

## 3. Async Image Processing with Celery

### Why?
- Don't block HTTP requests during image processing
- Handle batch operations efficiently
- Retry failed operations

```python
# products/tasks.py
from celery import shared_task
from .models import ProductImage
from .image_processor import ImageProcessor

@shared_task(bind=True, max_retries=3)
def process_product_image(self, image_id):
    """Process product image asynchronously"""
    try:
        image = ProductImage.objects.get(id=image_id)
        
        # Create variants
        variants = ImageProcessor.create_variants(image.image)
        
        # Save variants
        image.thumbnail = variants['thumbnail']
        image.image_small = variants['small']
        image.image_medium = variants['medium']
        image.image_large = variants['large']
        image.save()
        
        return f"Processed image {image_id}"
    
    except Exception as e:
        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=60 * (2 ** self.request.retries))

@shared_task
def cleanup_old_images(days=365):
    """Clean up images older than specified days"""
    from datetime import datetime, timedelta
    from django.utils import timezone
    
    cutoff_date = timezone.now() - timedelta(days=days)
    
    old_images = ProductImage.objects.filter(uploaded_at__lt=cutoff_date)
    count = old_images.count()
    
    # Delete files and records
    for image in old_images:
        image.delete()
    
    return f"Cleaned up {count} old images"
```

---

## 4. Malware Scanning Integration

### Option A: ClamAV (Self-hosted)

```python
# products/malware_scanner.py
import pyclamd
from django.core.exceptions import ValidationError
from django.conf import settings

class MalwareScanner:
    """Scan files for malware using ClamAV"""
    
    @staticmethod
    def scan_file(file_path):
        """Scan a file for malware"""
        if not settings.ENABLE_MALWARE_SCANNING:
            return True
        
        try:
            # Connect to ClamAV daemon
            cd = pyclamd.ClamdUnixSocket()
            
            # Scan file
            result = cd.scan_file(file_path)
            
            if result:
                # Malware detected
                virus_name = result[file_path][1]
                raise ValidationError(f'Malware detected: {virus_name}')
            
            return True
        
        except Exception as e:
            # Log error but don't block upload if scanner is down
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f'Malware scan failed: {str(e)}')
            
            # In production, you might want to quarantine the file
            # and notify admins instead of allowing upload
            return True
```

### Option B: VirusTotal API (Cloud-based)

```python
# products/malware_scanner.py
import requests
import hashlib
from django.conf import settings

class VirusTotalScanner:
    """Scan files using VirusTotal API"""
    
    API_URL = 'https://www.virustotal.com/api/v3'
    
    @staticmethod
    def scan_file_hash(file_path):
        """Scan file hash against VirusTotal database"""
        if not settings.VIRUSTOTAL_API_KEY:
            return True
        
        # Calculate file hash
        with open(file_path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        
        # Check hash
        headers = {'x-apikey': settings.VIRUSTOTAL_API_KEY}
        response = requests.get(
            f'{VirusTotalScanner.API_URL}/files/{file_hash}',
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            stats = data['data']['attributes']['last_analysis_stats']
            
            # Check if any scanner detected malware
            if stats['malicious'] > 0:
                raise ValidationError(
                    f'File flagged as malicious by {stats["malicious"]} scanners'
                )
        
        return True
```

**Recommendation**: Use **ClamAV** for cost-effectiveness, **VirusTotal** for additional verification of suspicious files.

---

## 5. Rate Limiting with Redis

### Current Issue:
- In-memory rate limiting doesn't work across multiple servers
- No persistent rate limit tracking

```python
# products/rate_limiter.py
import redis
from django.conf import settings
from django.core.cache import cache

class RateLimiter:
    """Redis-based rate limiting for file uploads"""
    
    def __init__(self):
        if settings.REDIS_URL:
            self.redis_client = redis.from_url(settings.REDIS_URL)
        else:
            self.redis_client = None
    
    def check_upload_limit(self, user_id, max_uploads=10, window_seconds=60):
        """Check if user has exceeded upload limit"""
        if not self.redis_client:
            # Fallback to Django cache
            return self._check_with_cache(user_id, max_uploads, window_seconds)
        
        key = f'upload_rate:{user_id}'
        
        # Increment counter
        count = self.redis_client.incr(key)
        
        # Set expiry on first increment
        if count == 1:
            self.redis_client.expire(key, window_seconds)
        
        return count <= max_uploads
    
    def check_upload_size_limit(self, user_id, file_size, max_size_mb=50, window_seconds=60):
        """Check if user has exceeded total upload size limit"""
        if not self.redis_client:
            return True
        
        key = f'upload_size:{user_id}'
        
        # Get current total
        current_total = self.redis_client.get(key)
        current_total = int(current_total) if current_total else 0
        
        # Add new file size
        new_total = current_total + file_size
        max_bytes = max_size_mb * 1024 * 1024
        
        if new_total > max_bytes:
            return False
        
        # Update total
        self.redis_client.set(key, new_total, ex=window_seconds)
        
        return True
    
    def _check_with_cache(self, user_id, max_uploads, window_seconds):
        """Fallback to Django cache"""
        key = f'upload_rate:{user_id}'
        count = cache.get(key, 0)
        
        if count >= max_uploads:
            return False
        
        cache.set(key, count + 1, window_seconds)
        return True

# Middleware
class FileUploadRateLimitMiddleware:
    """Middleware to enforce rate limits on file uploads"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limiter = RateLimiter()
    
    def __call__(self, request):
        # Check if this is a file upload request
        if request.method == 'POST' and request.FILES:
            user_id = request.user.id if request.user.is_authenticated else request.META.get('REMOTE_ADDR')
            
            # Check upload count limit
            if not self.rate_limiter.check_upload_limit(user_id):
                from django.http import JsonResponse
                return JsonResponse({
                    'error': 'Upload rate limit exceeded. Please try again later.'
                }, status=429)
            
            # Check upload size limit
            total_size = sum(f.size for f in request.FILES.values())
            if not self.rate_limiter.check_upload_size_limit(user_id, total_size):
                from django.http import JsonResponse
                return JsonResponse({
                    'error': 'Upload size limit exceeded. Please try again later.'
                }, status=429)
        
        return self.get_response(request)
```

---

## 6. Monitoring and Logging

```python
# products/monitoring.py
import logging
from django.conf import settings
from datetime import datetime

logger = logging.getLogger(__name__)

class FileUploadMonitor:
    """Monitor file upload activities"""
    
    @staticmethod
    def log_upload(user, file_name, file_size, file_type, success=True, error=None):
        """Log file upload attempt"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user.id if user else None,
            'user_email': user.email if user else None,
            'file_name': file_name,
            'file_size': file_size,
            'file_type': file_type,
            'success': success,
            'error': str(error) if error else None,
        }
        
        if success:
            logger.info(f'File upload successful: {log_data}')
        else:
            logger.warning(f'File upload failed: {log_data}')
        
        # Send to monitoring service (e.g., Sentry, DataDog)
        if settings.ENABLE_MONITORING:
            FileUploadMonitor._send_to_monitoring_service(log_data)
    
    @staticmethod
    def log_suspicious_activity(user, reason, details):
        """Log suspicious file upload activity"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user.id if user else None,
            'reason': reason,
            'details': details,
        }
        
        logger.error(f'Suspicious file upload activity: {log_data}')
        
        # Alert admins
        FileUploadMonitor._alert_admins(log_data)
    
    @staticmethod
    def _send_to_monitoring_service(data):
        """Send metrics to monitoring service"""
        # Implement integration with your monitoring service
        pass
    
    @staticmethod
    def _alert_admins(data):
        """Send alert to administrators"""
        # Implement admin notification
        pass
```

---

## 7. Backup Strategy

```python
# products/backup.py
from django.core.management.base import BaseCommand
from products.models import ProductImage
from orders.models import DynamicResourceSubmission
import boto3
from datetime import datetime

class Command(BaseCommand):
    help = 'Backup uploaded files to S3 Glacier for long-term storage'
    
    def handle(self, *args, **options):
        s3_client = boto3.client('s3')
        glacier_bucket = settings.AWS_GLACIER_BUCKET
        
        # Backup product images
        for image in ProductImage.objects.all():
            if image.image:
                self._backup_file(s3_client, image.image.path, glacier_bucket)
        
        # Backup user uploads
        for submission in DynamicResourceSubmission.objects.filter(file_value__isnull=False):
            if submission.file_value:
                self._backup_file(s3_client, submission.file_value.path, glacier_bucket)
        
        self.stdout.write(self.style.SUCCESS('Backup completed'))
    
    def _backup_file(self, s3_client, file_path, bucket):
        """Backup a single file to S3 Glacier"""
        key = f'backups/{datetime.now().strftime("%Y/%m/%d")}/{os.path.basename(file_path)}'
        
        s3_client.upload_file(
            file_path,
            bucket,
            key,
            ExtraArgs={'StorageClass': 'GLACIER'}
        )
```

---

## 8. Security Headers and CORS

```python
# settings.py - Production security settings

# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HTTPS settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CORS for file uploads
CORS_ALLOWED_ORIGINS = [
    'https://yourdomain.com',
    'https://admin.yourdomain.com',
]

CORS_ALLOW_CREDENTIALS = True

# File upload specific CORS
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'content-disposition',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
```

---

## 9. Database Optimization

```python
# products/models.py - Add indexes for better query performance

class ProductImage(models.Model):
    # ... existing fields ...
    
    class Meta:
        ordering = ['order', '-uploaded_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id', 'is_primary']),
            models.Index(fields=['content_type', 'object_id', 'order']),
            models.Index(fields=['-uploaded_at']),
            models.Index(fields=['is_primary', 'order']),
        ]

class DynamicResourceSubmission(models.Model):
    # ... existing fields ...
    
    class Meta:
        unique_together = ['order_item', 'field_definition']
        indexes = [
            models.Index(fields=['order_item', 'field_definition']),
            models.Index(fields=['-uploaded_at']),
        ]
```

---

## 10. Implementation Priority

### Phase 1 (Critical - Before Launch):
1. ✅ **CDN Integration** - AWS S3 + CloudFront
2. ✅ **Image Optimization** - Automatic compression and resizing
3. ✅ **Redis Rate Limiting** - Prevent abuse
4. ✅ **Monitoring & Logging** - Track all uploads

### Phase 2 (Important - First Month):
5. ✅ **Malware Scanning** - ClamAV integration
6. ✅ **Async Processing** - Celery for image processing
7. ✅ **Database Optimization** - Add indexes
8. ✅ **Security Headers** - HTTPS and CORS

### Phase 3 (Nice to Have - First Quarter):
9. ✅ **Backup Strategy** - S3 Glacier backups
10. ✅ **Advanced Monitoring** - Sentry/DataDog integration

---

## Estimated Costs (Monthly)

### AWS Infrastructure:
- **S3 Storage**: $0.023/GB (~$5-20 for 200-1000GB)
- **CloudFront**: $0.085/GB transfer (~$10-50 for 100-500GB)
- **Redis (ElastiCache)**: $15-50 (t3.micro to t3.small)
- **Total**: ~$30-120/month

### Alternative (Cloudinary):
- **Free Tier**: 25GB storage, 25GB bandwidth
- **Paid Plans**: $89/month for 100GB storage, 100GB bandwidth

**Recommendation**: Start with AWS for better scalability and cost control.

---

## Configuration Checklist

```bash
# .env.production
# AWS Configuration
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_STORAGE_BUCKET_NAME=your-bucket
AWS_S3_REGION_NAME=ap-south-1
AWS_CLOUDFRONT_DOMAIN=d1234567890.cloudfront.net

# Redis Configuration
REDIS_URL=redis://your-redis-host:6379/0

# Malware Scanning
ENABLE_MALWARE_SCANNING=True
VIRUSTOTAL_API_KEY=your_api_key

# Monitoring
ENABLE_MONITORING=True
SENTRY_DSN=your_sentry_dsn

# File Upload Limits
MAX_UPLOAD_SIZE_MB=10
MAX_UPLOADS_PER_MINUTE=10
MAX_TOTAL_SIZE_PER_MINUTE_MB=50

# Image Processing
IMAGE_QUALITY=85
MAX_IMAGE_WIDTH=1920
ENABLE_WEBP=True
```

---

## Next Steps

1. **Review and approve** this plan
2. **Set up AWS account** and create S3 bucket + CloudFront distribution
3. **Install dependencies**: `pip install boto3 django-storages pillow redis pyclamd`
4. **Implement Phase 1** features
5. **Test thoroughly** in staging environment
6. **Deploy to production** with monitoring

Would you like me to implement any of these features now?

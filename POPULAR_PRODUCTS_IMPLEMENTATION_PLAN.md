# Popular Products Feature - Implementation Plan

## 📋 Current Situation

### Problem:
- Popular Packages section shows first 3 packages (`.slice(0, 3)`)
- Popular Campaigns section shows first 3 campaigns (`.slice(0, 3)`)
- When new products are added, they automatically appear in "Popular" section
- No manual control over which products are featured

### Current Code:
```typescript
// suburbia/src/components/PackagesSection.tsx
const data = await productService.getPackages();
setPackages(data.slice(0, 3)); // Always shows first 3

// suburbia/src/components/CampaignsSection.tsx
const data = await productService.getCampaigns();
setCampaigns(data.slice(0, 3)); // Always shows first 3
```

---

## 🎯 Solution: "Popular" Toggle Feature

### Goal:
- Admin can mark any 3 packages as "popular"
- Admin can mark any 3 campaigns as "popular"
- Only marked products appear in Popular sections
- Toggle button in admin panel to mark/unmark products

---

## 📐 Implementation Plan

### Phase 1: Database Changes

#### 1.1 Add `is_popular` Field to Models
**File**: `backend/products/models.py`

```python
class Package(models.Model):
    # ... existing fields ...
    is_active = models.BooleanField(default=True)
    is_popular = models.BooleanField(default=False)  # NEW FIELD
    popular_order = models.IntegerField(default=0, help_text='Order in popular section (1-3)')  # NEW FIELD
    # ... rest of fields ...
    
    class Meta:
        ordering = ['popular_order', '-created_at']  # Popular first, then by date

class Campaign(models.Model):
    # ... existing fields ...
    is_active = models.BooleanField(default=True)
    is_popular = models.BooleanField(default=False)  # NEW FIELD
    popular_order = models.IntegerField(default=0, help_text='Order in popular section (1-3)')  # NEW FIELD
    # ... rest of fields ...
    
    class Meta:
        ordering = ['popular_order', '-created_at']  # Popular first, then by date
```

**Why `popular_order`?**
- Allows admin to control the order of popular items (1st, 2nd, 3rd position)
- More flexible than just boolean flag

#### 1.2 Create Migration
```bash
python manage.py makemigrations products
python manage.py migrate
```

---

### Phase 2: Backend API Changes

#### 2.1 Update Serializers
**File**: `backend/products/serializers.py`

```python
class PackageSerializer(serializers.ModelSerializer):
    # ... existing fields ...
    class Meta:
        model = Package
        fields = [
            'id', 'name', 'price', 'description', 'features', 
            'deliverables', 'items', 'is_active', 'is_popular',  # Add is_popular
            'popular_order', 'created_at', 'updated_at', 
            'created_by', 'created_by_name', 'images', 'primary_image', 'type'
        ]

class CampaignSerializer(serializers.ModelSerializer):
    # ... existing fields ...
    class Meta:
        model = Campaign
        fields = [
            'id', 'name', 'price', 'unit', 'description', 'features',
            'deliverables', 'is_active', 'is_popular',  # Add is_popular
            'popular_order', 'created_at', 'updated_at',
            'created_by', 'created_by_name', 'images', 'primary_image', 'type'
        ]
```

#### 2.2 Add Popular Endpoints
**File**: `backend/products/views.py`

```python
class PackageViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing packages"""
    queryset = Package.objects.filter(is_active=True).prefetch_related('items')
    serializer_class = PackageSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get popular packages (max 3)"""
        popular_packages = Package.objects.filter(
            is_active=True,
            is_popular=True
        ).order_by('popular_order', '-created_at')[:3]
        
        serializer = self.get_serializer(popular_packages, many=True)
        return Response(serializer.data)

class CampaignViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing campaigns"""
    queryset = Campaign.objects.filter(is_active=True)
    serializer_class = CampaignSerializer
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get popular campaigns (max 3)"""
        popular_campaigns = Campaign.objects.filter(
            is_active=True,
            is_popular=True
        ).order_by('popular_order', '-created_at')[:3]
        
        serializer = self.get_serializer(popular_campaigns, many=True)
        return Response(serializer.data)
```

**New Endpoints:**
- `GET /api/packages/popular/` - Returns popular packages
- `GET /api/campaigns/popular/` - Returns popular campaigns

#### 2.3 Add Admin Toggle Endpoints
**File**: `backend/admin_panel/views.py`

```python
@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def toggle_package_popular(request, pk):
    """Toggle package popular status"""
    try:
        package = Package.objects.get(id=pk)
        
        # If marking as popular, check if already have 3 popular packages
        if not package.is_popular:
            popular_count = Package.objects.filter(is_popular=True).count()
            if popular_count >= 3:
                return Response({
                    'error': 'Maximum 3 packages can be marked as popular. Please unmark one first.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Set as popular with next order
            max_order = Package.objects.filter(is_popular=True).aggregate(
                models.Max('popular_order')
            )['popular_order__max'] or 0
            package.is_popular = True
            package.popular_order = max_order + 1
        else:
            # Unmark as popular
            package.is_popular = False
            package.popular_order = 0
        
        package.save()
        
        # Reorder remaining popular packages
        popular_packages = Package.objects.filter(is_popular=True).order_by('popular_order')
        for idx, pkg in enumerate(popular_packages, 1):
            if pkg.popular_order != idx:
                pkg.popular_order = idx
                pkg.save()
        
        serializer = PackageSerializer(package, context={'request': request})
        return Response(serializer.data)
        
    except Package.DoesNotExist:
        return Response({'error': 'Package not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def toggle_campaign_popular(request, pk):
    """Toggle campaign popular status"""
    try:
        campaign = Campaign.objects.get(id=pk)
        
        # If marking as popular, check if already have 3 popular campaigns
        if not campaign.is_popular:
            popular_count = Campaign.objects.filter(is_popular=True).count()
            if popular_count >= 3:
                return Response({
                    'error': 'Maximum 3 campaigns can be marked as popular. Please unmark one first.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Set as popular with next order
            max_order = Campaign.objects.filter(is_popular=True).aggregate(
                models.Max('popular_order')
            )['popular_order__max'] or 0
            campaign.is_popular = True
            campaign.popular_order = max_order + 1
        else:
            # Unmark as popular
            campaign.is_popular = False
            campaign.popular_order = 0
        
        campaign.save()
        
        # Reorder remaining popular campaigns
        popular_campaigns = Campaign.objects.filter(is_popular=True).order_by('popular_order')
        for idx, cmp in enumerate(popular_campaigns, 1):
            if cmp.popular_order != idx:
                cmp.popular_order = idx
                cmp.save()
        
        serializer = CampaignSerializer(campaign, context={'request': request})
        return Response(serializer.data)
        
    except Campaign.DoesNotExist:
        return Response({'error': 'Campaign not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def reorder_popular_packages(request):
    """Reorder popular packages"""
    # Expects: { "order": [id1, id2, id3] }
    order = request.data.get('order', [])
    
    for idx, package_id in enumerate(order, 1):
        Package.objects.filter(id=package_id, is_popular=True).update(popular_order=idx)
    
    popular_packages = Package.objects.filter(is_popular=True).order_by('popular_order')
    serializer = PackageSerializer(popular_packages, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def reorder_popular_campaigns(request):
    """Reorder popular campaigns"""
    # Expects: { "order": [id1, id2, id3] }
    order = request.data.get('order', [])
    
    for idx, campaign_id in enumerate(order, 1):
        Campaign.objects.filter(id=campaign_id, is_popular=True).update(popular_order=idx)
    
    popular_campaigns = Campaign.objects.filter(is_popular=True).order_by('popular_order')
    serializer = CampaignSerializer(popular_campaigns, many=True, context={'request': request})
    return Response(serializer.data)
```

#### 2.4 Add URL Routes
**File**: `backend/admin_panel/urls.py`

```python
urlpatterns = [
    # ... existing routes ...
    
    # Popular toggle endpoints
    path('products/packages/<int:pk>/toggle-popular/', 
         toggle_package_popular, 
         name='toggle-package-popular'),
    path('products/campaigns/<int:pk>/toggle-popular/', 
         toggle_campaign_popular, 
         name='toggle-campaign-popular'),
    
    # Reorder popular products
    path('products/packages/reorder-popular/', 
         reorder_popular_packages, 
         name='reorder-popular-packages'),
    path('products/campaigns/reorder-popular/', 
         reorder_popular_campaigns, 
         name='reorder-popular-campaigns'),
]
```

---

### Phase 3: Admin Frontend Changes

#### 3.1 Update Product Service
**File**: `admin-frontend/src/services/productService.ts`

```typescript
// Add to ProductService class

async togglePackagePopular(packageId: number): Promise<Package> {
  const response = await api.patch(`/admin/products/packages/${packageId}/toggle-popular/`);
  return response.data;
}

async toggleCampaignPopular(campaignId: number): Promise<Campaign> {
  const response = await api.patch(`/admin/products/campaigns/${campaignId}/toggle-popular/`);
  return response.data;
}

async reorderPopularPackages(order: number[]): Promise<Package[]> {
  const response = await api.patch('/admin/products/packages/reorder-popular/', { order });
  return response.data;
}

async reorderPopularCampaigns(order: number[]): Promise<Campaign[]> {
  const response = await api.patch('/admin/products/campaigns/reorder-popular/', { order });
  return response.data;
}
```

#### 3.2 Add Popular Toggle Button
**File**: `admin-frontend/src/components/PopularToggleButton.tsx` (NEW FILE)

```typescript
import { Star, StarOff } from 'lucide-react';

interface PopularToggleButtonProps {
  isPopular: boolean;
  popularOrder?: number;
  onToggle: () => void;
  disabled?: boolean;
}

export function PopularToggleButton({
  isPopular,
  popularOrder,
  onToggle,
  disabled = false
}: PopularToggleButtonProps) {
  return (
    <button
      onClick={onToggle}
      disabled={disabled}
      className={`
        flex items-center gap-2 px-4 py-2 rounded-lg font-medium
        transition-all duration-200
        ${isPopular 
          ? 'bg-yellow-500 text-white hover:bg-yellow-600' 
          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
        }
        ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
      `}
    >
      {isPopular ? <Star className="w-5 h-5 fill-current" /> : <StarOff className="w-5 h-5" />}
      <span>
        {isPopular ? `Popular #${popularOrder}` : 'Mark as Popular'}
      </span>
    </button>
  );
}
```

#### 3.3 Update Package List Component
**File**: `admin-frontend/src/pages/PackageList.tsx`

Add popular toggle button to each package row:

```typescript
<PopularToggleButton
  isPopular={pkg.is_popular}
  popularOrder={pkg.popular_order}
  onToggle={() => handleTogglePopular(pkg.id)}
  disabled={!pkg.is_popular && popularCount >= 3}
/>
```

#### 3.4 Add Popular Badge
Show visual indicator for popular products in the list:

```typescript
{pkg.is_popular && (
  <span className="inline-flex items-center gap-1 px-2 py-1 bg-yellow-100 text-yellow-800 rounded-full text-xs font-medium">
    <Star className="w-3 h-3 fill-current" />
    Popular #{pkg.popular_order}
  </span>
)}
```

---

### Phase 4: Suburbia Frontend Changes

#### 4.1 Update Product Types
**File**: `suburbia/src/types/product.ts`

```typescript
export interface ProductImage {
  id: number;
  image: string;
  image_url: string;      // Add full URL
  thumbnail: string;
  thumbnail_url: string;  // Add full URL
  is_primary: boolean;
  order: number;
  alt_text: string;
}

export interface Package {
  id: number;
  name: string;
  price: number;
  description: string;
  items: PackageItem[];
  features?: string[];
  deliverables?: string[];
  is_active: boolean;
  is_popular?: boolean;        // NEW
  popular_order?: number;      // NEW
  created_at: string;
  images?: ProductImage[];
  primary_image?: ProductImage; // NEW - Primary image from backend
}

export interface Campaign {
  id: number;
  name: string;
  price: number;
  unit: string;
  description: string;
  features?: string[];
  deliverables?: string[];
  is_active: boolean;
  is_popular?: boolean;        // NEW
  popular_order?: number;      // NEW
  created_at: string;
  images?: ProductImage[];
  primary_image?: ProductImage; // NEW - Primary image from backend
}
```

#### 4.2 Update Product Service
**File**: `suburbia/src/services/productService.ts`

```typescript
// Add new methods

async getPopularPackages(): Promise<Package[]> {
  const response = await api.get<Package[]>('/packages/popular/');
  return response.data;
}

async getPopularCampaigns(): Promise<Campaign[]> {
  const response = await api.get<Campaign[]>('/campaigns/popular/');
  return response.data;
}
```

#### 4.3 Update PackagesSection Component
**File**: `suburbia/src/components/PackagesSection.tsx`

```typescript
// Change from:
const data = await productService.getPackages();
setPackages(data.slice(0, 3));

// To:
const data = await productService.getPopularPackages();
setPackages(data); // Already limited to 3 by backend

// Add image display (if not already present)
// In PackageCard component:
{pkg.primary_image && (
  <img 
    src={pkg.primary_image.image_url} 
    alt={pkg.primary_image.alt_text || pkg.name}
    className="w-full h-auto object-cover"
  />
)}
```

#### 4.4 Update CampaignsSection Component
**File**: `suburbia/src/components/CampaignsSection.tsx`

```typescript
// Change from:
const data = await productService.getCampaigns();
setCampaigns(data.slice(0, 3));

// To:
const data = await productService.getPopularCampaigns();
setCampaigns(data); // Already limited to 3 by backend

// Add image display (if not already present)
// In CampaignCard component:
{campaign.primary_image && (
  <img 
    src={campaign.primary_image.image_url} 
    alt={campaign.primary_image.alt_text || campaign.name}
    className="w-full h-auto object-cover"
  />
)}
```

#### 4.5 Add Image Display Helper
**File**: `suburbia/src/utils/imageHelpers.ts` (NEW FILE)

```typescript
import { ProductImage } from '@/types/product';

/**
 * Get the primary image URL from a product
 * Falls back to first image if no primary image is set
 */
export function getPrimaryImageUrl(
  primaryImage?: ProductImage,
  images?: ProductImage[]
): string | null {
  // First try primary image
  if (primaryImage?.image_url) {
    return primaryImage.image_url;
  }
  
  // Fall back to first image
  if (images && images.length > 0) {
    return images[0].image_url;
  }
  
  return null;
}

/**
 * Get the primary thumbnail URL from a product
 * Falls back to first thumbnail if no primary image is set
 */
export function getPrimaryThumbnailUrl(
  primaryImage?: ProductImage,
  images?: ProductImage[]
): string | null {
  // First try primary image thumbnail
  if (primaryImage?.thumbnail_url) {
    return primaryImage.thumbnail_url;
  }
  
  // Fall back to first image thumbnail
  if (images && images.length > 0) {
    return images[0].thumbnail_url;
  }
  
  return null;
}
```

**Usage in components:**
```typescript
import { getPrimaryImageUrl } from '@/utils/imageHelpers';

// In component:
const imageUrl = getPrimaryImageUrl(pkg.primary_image, pkg.images);

{imageUrl && (
  <img 
    src={imageUrl} 
    alt={pkg.primary_image?.alt_text || pkg.name}
    className="w-full h-auto object-cover"
  />
)}
```

---

## 🎨 UI/UX Design

### Admin Panel - Package/Campaign List View

```
┌─────────────────────────────────────────────────────────────┐
│ Packages                                          [+ Add New] │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Basic Package                    ₹5,000  [★ Popular #1] │ │
│ │ Created: 2024-01-15              Active  [Edit] [Delete] │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                               │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Premium Package                  ₹10,000 [★ Popular #2] │ │
│ │ Created: 2024-01-14              Active  [Edit] [Delete] │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                               │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ Advanced Package                 ₹15,000 [☆ Mark Popular]│ │
│ │ Created: 2024-01-13              Active  [Edit] [Delete] │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                               │
└─────────────────────────────────────────────────────────────┘

Legend:
★ = Currently popular (yellow button)
☆ = Not popular (gray button)
```

### Behavior:
- **Click "Mark as Popular"**: Marks product as popular
- **Click "Popular #X"**: Unmarks product from popular
- **Maximum 3**: Can't mark more than 3 as popular
- **Auto-reorder**: When unmarking, remaining products reorder automatically

---

## 📊 Database Schema Changes

### Before:
```sql
CREATE TABLE products_package (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200),
    price DECIMAL(10,2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP,
    ...
);
```

### After:
```sql
CREATE TABLE products_package (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200),
    price DECIMAL(10,2),
    is_active BOOLEAN DEFAULT TRUE,
    is_popular BOOLEAN DEFAULT FALSE,      -- NEW
    popular_order INTEGER DEFAULT 0,       -- NEW
    created_at TIMESTAMP,
    ...
);

CREATE INDEX idx_package_popular ON products_package(is_popular, popular_order);
```

---

## 🧪 Testing Plan

### Backend Tests:
1. Test marking package as popular
2. Test unmarking package from popular
3. Test maximum 3 popular limit
4. Test auto-reordering
5. Test popular endpoint returns correct data
6. Test popular endpoint respects order

### Frontend Tests:
1. Test toggle button works
2. Test visual feedback (star icon)
3. Test disabled state when limit reached
4. Test popular section shows correct products
5. Test popular section respects order

---

## 🚀 Deployment Steps

### Step 1: Backend
```bash
# 1. Create migration
python manage.py makemigrations products

# 2. Apply migration
python manage.py migrate

# 3. Mark initial popular products (optional)
python manage.py shell
>>> from products.models import Package, Campaign
>>> Package.objects.filter(id__in=[1,2,3]).update(is_popular=True)
>>> for i, pkg in enumerate(Package.objects.filter(is_popular=True), 1):
...     pkg.popular_order = i
...     pkg.save()
```

### Step 2: Admin Frontend
```bash
# Update code and restart
npm run dev
```

### Step 3: Suburbia Frontend
```bash
# Update code and restart
npm run dev
```

---

## ✅ Success Criteria

- [ ] Admin can mark any 3 packages as popular
- [ ] Admin can mark any 3 campaigns as popular
- [ ] Maximum 3 popular products enforced
- [ ] Popular section shows only marked products
- [ ] Popular section respects order (1, 2, 3)
- [ ] Toggle button shows correct state
- [ ] Visual feedback (star icon) works
- [ ] Auto-reordering works when unmarking
- [ ] **Primary image displayed** for all products (first uploaded/marked as primary)
- [ ] **Image fallback** works (first image if no primary)
- [ ] **Cloudinary URLs** used for all images
- [ ] No breaking changes to existing functionality

---

## 📝 Notes

### Image Display Strategy
**Backend provides:**
- `primary_image` - The image marked as primary (or first uploaded)
- `images[]` - Array of all images ordered by `order` field

**Frontend displays:**
1. **First choice**: `primary_image.image_url` (Cloudinary URL)
2. **Fallback**: `images[0].image_url` (first image if no primary)
3. **No image**: Show placeholder or hide image section

**Why primary_image?**
- Backend already provides it in serializer
- Automatically set when first image uploaded
- Admin can change primary image in admin panel
- Consistent across all product displays

### Why This Approach?
1. **Flexible**: Admin has full control
2. **Scalable**: Easy to change limit from 3 to any number
3. **Ordered**: Products appear in specific order
4. **Simple**: Clear UI/UX for admins
5. **Performant**: Indexed queries for fast lookups
6. **Image-ready**: Primary image automatically included

### Alternative Approaches Considered:
1. **Date-based**: Show newest 3 (current) - ❌ No control
2. **View count**: Show most viewed - ❌ Complex tracking
3. **Manual list**: Separate popular table - ❌ Over-engineered
4. **Boolean only**: Just is_popular flag - ❌ No ordering control

### Future Enhancements:
- Drag-and-drop reordering in admin panel
- Analytics on popular product performance
- A/B testing different popular products
- Scheduled popular product rotation
- Popular products by category/region

---

## 🎯 Implementation Order

1. ✅ **Phase 1**: Database changes (migration)
2. ✅ **Phase 2**: Backend API (endpoints)
3. ✅ **Phase 3**: Admin frontend (toggle button)
4. ✅ **Phase 4**: Suburbia frontend (fetch popular)
5. ✅ **Testing**: All components
6. ✅ **Deployment**: Production

**Estimated Time**: 4-6 hours total
- Phase 1: 30 minutes
- Phase 2: 1.5 hours
- Phase 3: 1.5 hours
- Phase 4: 30 minutes
- Testing: 1 hour
- Documentation: 30 minutes

---

## 📚 Documentation Updates Needed

- [ ] Update API documentation with new endpoints
- [ ] Update admin user guide with popular feature
- [ ] Update README with popular feature description
- [ ] Add screenshots to documentation
- [ ] Update changelog

---

**Ready to implement? Let me know and I'll start with Phase 1!** 🚀

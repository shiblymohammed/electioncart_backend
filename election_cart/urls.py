"""
URL configuration for election_cart project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.db import connection
from django.utils import timezone
import logging

from admin_panel.views import StaffOrderListView, StaffOrderDetailView, update_checklist_item

logger = logging.getLogger(__name__)


def health_check(request):
    """
    Health check endpoint for monitoring system status.
    
    Returns:
        - 200 OK: System is healthy (database connected)
        - 503 Service Unavailable: System is unhealthy (database disconnected)
    
    Response format:
        {
            "status": "healthy" | "unhealthy",
            "service": "election-cart-api",
            "database": "connected" | "disconnected",
            "timestamp": "2025-11-03T14:23:45Z"
        }
    """
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        
        response_data = {
            'status': 'healthy',
            'service': 'election-cart-api',
            'database': 'connected',
            'timestamp': timezone.now().isoformat()
        }
        
        logger.info("Health check passed - system healthy")
        return JsonResponse(response_data, status=200)
        
    except Exception as e:
        response_data = {
            'status': 'unhealthy',
            'service': 'election-cart-api',
            'database': 'disconnected',
            'error': str(e),
            'timestamp': timezone.now().isoformat()
        }
        
        logger.error(f"Health check failed - database error: {e}", exc_info=True)
        return JsonResponse(response_data, status=503)


urlpatterns = [
    # Health check endpoint (no authentication required)
    path('health/', health_check, name='health-check'),
    
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/', include('products.urls')),
    path('api/cart/', include('cart.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/admin/', include('admin_panel.urls')),
    # Staff endpoints
    path('api/staff/orders/', StaffOrderListView.as_view(), name='staff-order-list'),
    path('api/staff/orders/<int:pk>/', StaffOrderDetailView.as_view(), name='staff-order-detail'),
    path('api/staff/checklist/<int:item_id>/', update_checklist_item, name='staff-checklist-update'),
    # Secure file serving
    path('api/secure-files/', include('products.file_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

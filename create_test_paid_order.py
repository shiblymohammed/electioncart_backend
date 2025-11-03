#!/usr/bin/env python
"""
Script to create a test paid order for testing invoice download
"""
import os
import django
import sys
from decimal import Decimal

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'election_cart.settings')
django.setup()

from orders.models import Order, OrderItem, PaymentHistory
from authentication.models import CustomUser
from products.models import Package, Campaign
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

def create_test_paid_order():
    # Get or create a test user
    try:
        user = CustomUser.objects.get(phone_number='+919999999999')
        print(f"✅ Using existing user: {user.phone_number}")
    except CustomUser.DoesNotExist:
        user = CustomUser.objects.create(
            phone_number='+919999999999',
            username='testuser_' + timezone.now().strftime('%Y%m%d%H%M%S'),
            role='customer'
        )
        print(f"✅ Created test user: {user.phone_number}")
    
    # Get a package or campaign
    package = Package.objects.filter(is_active=True).first()
    if not package:
        print("❌ No active packages found. Please create a package first.")
        return
    
    print(f"✅ Using package: {package.name}")
    
    # Create order
    order = Order.objects.create(
        user=user,
        total_amount=package.price,
        status='completed',
        razorpay_order_id='test_order_' + timezone.now().strftime('%Y%m%d%H%M%S')
    )
    print(f"✅ Created order: {order.order_number}")
    
    # Create order item
    content_type = ContentType.objects.get_for_model(Package)
    OrderItem.objects.create(
        order=order,
        content_type=content_type,
        object_id=package.id,
        quantity=1,
        price=package.price
    )
    print(f"✅ Added order item: {package.name}")
    
    # Create payment history
    payment_history = PaymentHistory.objects.create(
        order=order,
        status='success',
        payment_method='razorpay',
        transaction_id='test_txn_' + timezone.now().strftime('%Y%m%d%H%M%S'),
        amount=package.price,
        currency='INR',
        payment_date=timezone.now(),
        invoice_number=f'INV-{order.order_number}'
    )
    print(f"✅ Created payment history: {payment_history.invoice_number}")
    
    print("\n" + "="*60)
    print("✅ TEST ORDER CREATED SUCCESSFULLY!")
    print("="*60)
    print(f"Order ID: {order.id}")
    print(f"Order Number: {order.order_number}")
    print(f"User: {user.phone_number}")
    print(f"Amount: ₹{order.total_amount}")
    print(f"Status: {order.status}")
    print(f"Invoice Number: {payment_history.invoice_number}")
    print("\nYou can now:")
    print(f"1. Login as {user.phone_number} in Suburbia frontend")
    print(f"2. Go to Profile → My Orders")
    print(f"3. You should see the 'Download Invoice' button")
    print(f"\nOr in Admin Panel:")
    print(f"1. Go to Orders → View Order #{order.order_number}")
    print(f"2. You should see the 'Download Invoice' button in the header")
    print("="*60)

if __name__ == '__main__':
    try:
        create_test_paid_order()
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

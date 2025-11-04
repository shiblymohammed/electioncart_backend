# Payment Status Feature

## Overview
Added comprehensive payment status tracking for all orders in the ElectionCart system.

## Changes Made

### 1. Database Model Updates (`orders/models.py`)

#### New Field
- `payment_status`: CharField with choices:
  - `unpaid`: No payment received
  - `partial`: Partially paid
  - `paid`: Fully paid
  - `refunded`: Payment refunded
  - `cod`: Cash on Delivery

#### New Methods
- `get_total_paid()`: Calculate total amount paid from payment records
- `get_payment_balance()`: Calculate remaining balance
- `update_payment_status()`: Automatically update payment status based on payment records

### 2. API Serializers

#### OrderSerializer (`orders/serializers.py`)
Added fields:
- `payment_status`
- `total_paid`
- `payment_balance`

#### AdminOrderListSerializer (`admin_panel/serializers.py`)
Added fields:
- `payment_status`
- `total_paid`
- `payment_balance`

#### AdminOrderDetailSerializer (`admin_panel/serializers.py`)
Added field:
- `payment_status`

### 3. API Endpoints

#### New Endpoint
**POST** `/api/admin/orders/{id}/update-payment-status/`
- Manually update payment status
- Body: `{ "payment_status": "paid" }`
- Valid statuses: `unpaid`, `partial`, `paid`, `refunded`, `cod`

#### Updated Endpoints
- **POST** `/api/admin/orders/{id}/record-payment/`: Now automatically updates payment status
- **POST** `/api/orders/{id}/payment-success/`: Sets payment_status to 'paid' on successful Razorpay payment
- **POST** `/api/admin/orders/manual/`: Accepts payment_status in request body

### 4. Automatic Payment Status Updates

Payment status is automatically updated when:
1. Recording a payment via admin panel
2. Verifying Razorpay payment
3. Creating manual orders with payment information

### 5. Migration
- Migration file: `orders/migrations/0008_add_payment_status.py`
- Adds `payment_status` field with default value 'unpaid'

## Usage Examples

### Create Manual Order with Payment Status
```json
POST /api/admin/orders/manual/
{
  "customer": {
    "name": "John Doe",
    "phone": "+919876543210",
    "email": "john@example.com"
  },
  "items": [...],
  "payment_status": "paid",
  "payment_method": "cash",
  "payment_amount": 5000
}
```

### Record Payment (Auto-updates status)
```json
POST /api/admin/orders/123/record-payment/
{
  "amount": 2500,
  "payment_method": "upi",
  "payment_reference": "UPI123456"
}
```

### Manually Update Payment Status
```json
POST /api/admin/orders/123/update-payment-status/
{
  "payment_status": "paid"
}
```

### Get Order with Payment Info
```json
GET /api/orders/123/
Response:
{
  "id": 123,
  "order_number": "EC-20241104-ABC123",
  "total_amount": 5000.00,
  "payment_status": "partial",
  "total_paid": 2500.00,
  "payment_balance": 2500.00,
  ...
}
```

## Benefits

1. **Clear Payment Tracking**: Know at a glance which orders are paid, unpaid, or partially paid
2. **Automatic Updates**: Payment status updates automatically when payments are recorded
3. **Balance Calculation**: Easily see remaining balance for partial payments
4. **Manual Override**: Admins can manually update payment status when needed
5. **COD Support**: Special status for cash-on-delivery orders
6. **Refund Tracking**: Track refunded orders separately

## Frontend Integration

The frontend can now:
- Display payment status badges on order lists
- Show payment progress bars for partial payments
- Filter orders by payment status
- Display remaining balance prominently
- Show payment history with running totals

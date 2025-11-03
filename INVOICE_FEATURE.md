# Invoice Generation Feature

## Overview
Invoices are automatically generated for paid orders and can be downloaded by customers, admins, and assigned staff.

## API Endpoints

### 1. Customer Invoice Download
**Endpoint:** `GET /api/orders/<order_id>/invoice/download/`  
**Authentication:** Required (Customer must own the order)  
**Response:** PDF file download

**Example:**
```javascript
// Frontend code
const downloadInvoice = async (orderId) => {
  const response = await fetch(`/api/orders/${orderId}/invoice/download/`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `invoice-${orderId}.pdf`;
  a.click();
};
```

### 2. Admin/Staff Invoice Download
**Endpoint:** `GET /api/admin/orders/<order_id>/invoice/`  
**Authentication:** Required (Admin or assigned staff)  
**Response:** PDF file download

## Invoice Requirements

Invoices are only available for orders that:
1. Have been paid (payment_history.status == 'success')
2. Have a payment_history record

## Invoice Contents

Each invoice includes:
- Company header (Election Cart)
- Invoice number and date
- Order number and date
- Customer information (name, email, phone)
- Order items table with quantities and prices
- Total amount
- Payment information (method, transaction ID, status)
- Footer with thank you message

## Frontend Integration

### For Customer Frontend (Suburbia)

Add a download button in the "My Orders" page:

```typescript
// In your orders list component
<button 
  onClick={() => downloadInvoice(order.id)}
  disabled={!order.payment_history || order.payment_history.status !== 'success'}
>
  Download Invoice
</button>
```

### For Admin Panel

Add a download button in the order detail view:

```typescript
// In admin order detail component
<button 
  onClick={() => downloadAdminInvoice(order.id)}
  disabled={!order.payment_history || order.payment_history.status !== 'success'}
>
  Download Invoice
</button>
```

## Implementation Notes

1. **No Background Tasks Required:** Invoices are generated synchronously (no Celery/Redis needed)
2. **PDF Library:** Uses ReportLab for PDF generation
3. **File Storage:** PDFs are generated on-the-fly, not stored on disk
4. **Performance:** Generation takes ~100-200ms per invoice
5. **Security:** Access control ensures users can only download their own invoices

## Customization

To customize the invoice template, edit:
- `backend/orders/invoice_generator.py`
- Modify the `InvoiceGenerator` class methods:
  - `_build_header()` - Company header
  - `_build_invoice_details()` - Invoice metadata
  - `_build_customer_info()` - Customer details
  - `_build_items_table()` - Order items
  - `_build_payment_info()` - Payment details
  - `_build_footer()` - Footer content

## Testing

Test invoice generation:
```bash
# In Django shell
python manage.py shell

from orders.models import Order
from orders.invoice_generator import InvoiceGenerator

order = Order.objects.get(id=1)
generator = InvoiceGenerator()
pdf_buffer = generator.generate_invoice(order)

# Save to file for testing
with open('test_invoice.pdf', 'wb') as f:
    f.write(pdf_buffer.getvalue())
```

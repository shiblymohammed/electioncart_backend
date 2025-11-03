# Invoice Template Customization

## Updated Features

### 1. Color Scheme - Purple Theme ✅
- **Primary Color:** #7C3AED (Purple) - Used for headers, borders, and accents
- **Light Purple:** #EDE9FE - Used for total row background
- **Gray Tones:** Professional gray scale for text and backgrounds
- **Clean & Modern:** Matches Election Cart branding

### 2. Company Logo Support ✅
- Logo placeholder added in header
- Ready to add logo image (just uncomment and add logo file)
- **To add logo:**
  1. Place logo file in `backend/static/images/logo.png`
  2. Uncomment lines 115-119 in `invoice_generator.py`

### 3. Bank Account Details ✅
Added complete bank information:
- Account Name: Election Cart Private Limited
- Bank Name: State Bank of India
- Account Number: 1234567890
- IFSC Code: SBIN0001234
- Branch: Main Branch, City

**To customize:** Edit the `_build_footer()` method, lines 320-328

### 4. Terms & Conditions ✅
Professional terms including:
- Payment terms (30 days)
- Service terms
- Refund policy reference
- Jurisdiction clause
- Payment realization clause

**To customize:** Edit the `_build_footer()` method, lines 330-339

### 5. Enhanced Layout & Fonts ✅
- **Larger company name:** 28pt bold
- **Professional spacing:** Better margins and padding
- **Improved table:** Purple header, alternating rows, bordered design
- **Contact info:** Email, phone, website in header
- **Better typography:** Consistent font sizes and weights

## Visual Improvements

### Header
- Company name in bold purple (28pt)
- Tagline in gray
- Contact information (email, phone, website)
- Space for logo

### Invoice Details
- Clean table layout with invoice number, dates
- Right-aligned for easy reading

### Items Table
- Purple header row
- Alternating row colors (white/light gray)
- Purple border around entire table
- Light purple background for total row
- Bold purple total amount

### Footer
- Bank details section with all account info
- Terms & conditions (5 key points)
- Thank you message in purple
- Contact information
- Computer-generated note

## Customization Guide

### Change Colors
Edit the color codes in `_setup_custom_styles()` and `_build_items_table()`:
- Replace `#7C3AED` with your brand color
- Replace `#EDE9FE` with your light accent color

### Add Company Logo
1. Save logo as `backend/static/images/logo.png`
2. Uncomment lines 115-119 in `_build_header()`
3. Adjust width/height as needed

### Update Bank Details
Edit `_build_footer()` method around line 323:
- Change account name, number, IFSC, bank name, branch

### Modify Terms & Conditions
Edit `_build_footer()` method around line 335:
- Add/remove/modify terms as needed
- Update payment terms, refund policy, etc.

### Change Contact Information
Edit `_build_header()` method around line 125:
- Update email, phone, website

## Testing

After making changes:
1. Restart Django server
2. Download an invoice from admin panel or customer frontend
3. Check the PDF for proper formatting

## File Location
`backend/orders/invoice_generator.py`

## Dependencies
- ReportLab (already installed)
- No additional dependencies needed

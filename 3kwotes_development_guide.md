# 3kwotes MVP Development Guide
**Frappe Framework Implementation - 1 Day Sprint**

## Overview
Build a working MVP for 3kwotes - a business service request platform where users can submit service requests, receive BOQ (Bill of Quantities), and get quotes from verified vendors.

## Pre-requisites
- Frappe bench setup completed
- threequotes app created and installed
- ERPNext and Frappe apps available for reference
- Developer mode enabled

## Architecture Overview
```
User Journey: Landing Page → Category Selection → AI Chat → BOQ Generation → Vendor Dispatch → Quote Collection
```

## DocTypes to Create (Core Data Models)

### 1. Service Category
**Purpose**: Define available service categories
**Fields**:
- Category Name (Data, Mandatory) - e.g., "Printing", "Accounting", "Digital Marketing"
- Description (Text)
- AI Prompt Template (Long Text) - Category-specific questions
- Status (Select: Active/Inactive)
- Icon (Data) - For UI display

### 2. Service Request
**Purpose**: Main transaction document
**Fields**:
- Request ID (Auto-generated)
- Customer Name (Data, Mandatory)
- Customer Email (Data, Mandatory)
- Customer Phone (Data)
- Service Category (Link to Service Category)
- Chat Transcript (Long Text)
- BOQ Generated (Text Editor)
- Status (Select: Draft/BOQ Generated/Sent to Vendors/Quotes Received/Completed)
- Created Date (Date)
- BOQ PDF (Attach)

### 3. Vendor
**Purpose**: Manage vendor database
**Fields**:
- Vendor Name (Data, Mandatory)
- Email (Data, Mandatory)
- Phone (Data)
- Service Categories (Table - Multiple Link to Service Category)
- Status (Select: Active/Inactive)
- Rating (Rating)
- Response Time (Int) - in hours

### 4. Quote Response
**Purpose**: Store vendor responses
**Fields**:
- Service Request (Link to Service Request)
- Vendor (Link to Vendor)
- Quote Amount (Currency)
- Quote Details (Text Editor)
- Response Date (Date)
- Status (Select: Pending/Submitted/Accepted/Rejected)
- Attachment (Attach)

### 5. BOQ Template
**Purpose**: Templates for different service categories
**Fields**:
- Category (Link to Service Category)
- Template Name (Data)
- Template Content (Long Text)
- Variables (Small Text) - JSON format for dynamic fields

## Web Pages to Create

### 1. Landing Page (`templates/pages/index.html`)
- Hero section with value proposition
- Service categories display
- "Get Quotes" CTA button
- Simple, clean design

### 2. Service Request Form (`templates/pages/request.html`)
- Category selection dropdown
- Customer details form
- Integration with chat interface
- Progress indicator

### 3. Chat Interface (`templates/pages/chat.html`)
- AI-powered chat interface
- Category-specific question flow
- Real-time BOQ generation preview
- Confirmation step

### 4. Vendor Portal (`templates/pages/vendor.html`)
- Vendor login/registration
- View assigned BOQs
- Submit quotes
- Track response status

## Day 1 Implementation Plan

### Phase 1: Foundation (2 hours)
**Morning 9-11 AM**

1. **Setup & Configuration**
   ```bash
   # Enable developer mode if not already done
   bench set-config -g developer_mode true
   
   # Create site if not exists
   bench --site your-site.localhost install-app threequotes
   ```

2. **Create Core DocTypes**
   - Service Category
   - Vendor
   - Service Request
   - Quote Response
   - BOQ Template

3. **Initial Data Setup**
   - Create 3 service categories: Printing, Accounting, Digital Marketing
   - Add 3 sample vendors per category
   - Create BOQ templates for each category

### Phase 2: Core Functionality (3 hours)
**Morning 11 AM - 2 PM**

1. **Service Request Controller** (`service_request.py`)
   ```python
   # Add BOQ generation logic
   # Email sending functionality
   # Status management
   ```

2. **Web Forms Creation**
   - Customer request form
   - Vendor response form
   - Auto-email triggers

3. **Basic AI Integration**
   - Simple form-based "chat" (can be enhanced later)
   - Category-specific question sets
   - BOQ template population

### Phase 3: Web Interface (2 hours)
**Afternoon 2-4 PM**

1. **Landing Page Development**
   - Clean, professional design
   - Category showcase
   - Clear CTA buttons

2. **Request Flow Pages**
   - Category selection
   - Customer details form
   - BOQ preview and confirmation

3. **Basic Styling**
   - Use Bootstrap 4 (comes with Frappe)
   - Responsive design
   - Brand colors and typography

### Phase 4: Vendor & Admin Features (2 hours)
**Afternoon 4-6 PM**

1. **Vendor Portal**
   - Login system (use Frappe's built-in auth)
   - BOQ viewing interface
   - Quote submission form

2. **Admin Dashboard**
   - Service Request management
   - Vendor management
   - Basic analytics/reporting

3. **Email Integration**
   - BOQ dispatch to vendors
   - Quote received notifications
   - Customer updates

### Phase 5: Testing & Polish (1 hour)
**Evening 6-7 PM**

1. **End-to-End Testing**
   - Complete user journey
   - Email functionality
   - Form validations

2. **Basic Error Handling**
   - Form validation messages
   - Email failure handling
   - User-friendly error pages

## Quick Implementation Tips

### Leverage Existing Frappe Features
1. **Use Web Forms**: Instead of building custom forms, use Frappe's Web Form feature
2. **Email Integration**: Use Frappe's built-in email system
3. **User Management**: Leverage Frappe's user and permission system
4. **File Handling**: Use Frappe's file attachment system for BOQ PDFs

### Pre-built Components to Use
1. **From ERPNext**:
   - Customer/Supplier management patterns
   - Quotation workflow concepts
   - Email templates

2. **From Frappe**:
   - Web form templates
   - Email queue system
   - PDF generation utilities

### Simplified AI Integration (MVP Level)
Instead of complex AI chat:
1. Use form-based progressive questions
2. Category-specific question sets
3. Simple template-based BOQ generation
4. Can be enhanced with actual AI later

## File Structure
```
threequotes/
├── threequotes/
│   ├── doctype/
│   │   ├── service_category/
│   │   ├── service_request/
│   │   ├── vendor/
│   │   ├── quote_response/
│   │   └── boq_template/
│   ├── web_form/
│   │   ├── service_request_form/
│   │   └── vendor_quote_form/
│   └── templates/
│       ├── pages/
│       │   ├── index.html
│       │   ├── request.html
│       │   ├── chat.html
│       │   └── vendor.html
│       └── includes/
├── public/
│   ├── css/
│   │   └── threequotes.css
│   └── js/
│       └── threequotes.js
└── hooks.py
```

## Key Implementation Notes

### 1. Keep It Simple
- Focus on working functionality over perfect UX
- Use Frappe's default styling initially
- Implement basic features that work end-to-end

### 2. Leverage Existing Code
- Copy patterns from ERPNext Quotation doctype
- Use Frappe's email templates
- Adapt existing web form structures

### 3. MVP Shortcuts
- Static vendor assignment instead of complex matching
- Form-based "chat" instead of real AI initially
- Email-based quote collection instead of complex portal

### 4. Essential Hooks Configuration
```python
# In hooks.py
web_include_css = ["assets/css/threequotes.css"]
web_include_js = ["assets/js/threequotes.js"]

# Email templates
fixtures = ["Email Template"]
```

## Success Metrics for Day 1
- [ ] User can submit service request
- [ ] BOQ is generated and displayed
- [ ] Vendors receive email with BOQ
- [ ] Basic admin can manage requests
- [ ] Landing page is functional
- [ ] End-to-end flow works

## Post-MVP Enhancements (Day 2+)
- Real AI chat integration
- Advanced vendor matching
- Better UI/UX design
- Mobile responsiveness
- Advanced analytics
- Payment integration
- Review system

## Troubleshooting Guide
1. **Email not sending**: Check email configuration in site config
2. **Web forms not working**: Ensure permissions are set correctly
3. **Static files not loading**: Run `bench build` and check file paths
4. **DocType errors**: Clear cache and reload

---

**Remember**: The goal is a working MVP, not a perfect product. Focus on core functionality and user journey completion. 
# 3kwotes MVP - Quick Start Commands

## Immediate Setup (First 15 minutes)

### 1. Verify Setup
```bash
# Check if bench is working
bench --version

# Check if threequotes app exists
ls apps/threequotes

# Check if site is running
bench --site your-site.localhost list-apps
```

### 2. Essential Commands
```bash
# Start development server
bench start

# Enable developer mode (if not already done)
bench set-config -g developer_mode true

# Clear cache when needed
bench --site your-site.localhost clear-cache

# Build assets
bench build

# Access database console
bench --site your-site.localhost mariadb

# Access python console
bench --site your-site.localhost console
```

### 3. Create DocTypes (Use these exact field configurations)

#### Service Category DocType
```
Name: Service Category
Module: threequotes
Fields:
1. category_name (Data, Mandatory, Label: Category Name)
2. description (Text, Label: Description)
3. ai_prompt_template (Long Text, Label: AI Prompt Template)
4. status (Select, Label: Status, Options: Active\nInactive, Default: Active)
5. icon (Data, Label: Icon)
```

#### Vendor DocType
```
Name: Vendor
Module: threequotes
Fields:
1. vendor_name (Data, Mandatory, Label: Vendor Name)
2. email (Data, Mandatory, Label: Email)
3. phone (Data, Label: Phone)
4. service_categories (Table, Label: Service Categories)
5. status (Select, Label: Status, Options: Active\nInactive, Default: Active)
6. rating (Rating, Label: Rating)
7. response_time (Int, Label: Response Time (Hours))
```

#### Service Request DocType
```
Name: Service Request
Module: threequotes
Fields:
1. customer_name (Data, Mandatory, Label: Customer Name)
2. customer_email (Data, Mandatory, Label: Customer Email)
3. customer_phone (Data, Label: Customer Phone)
4. service_category (Link, Label: Service Category, Options: Service Category)
5. chat_transcript (Long Text, Label: Chat Transcript)
6. boq_generated (Text Editor, Label: BOQ Generated)
7. status (Select, Label: Status, Options: Draft\nBOQ Generated\nSent to Vendors\nQuotes Received\nCompleted, Default: Draft)
8. created_date (Date, Label: Created Date, Default: Today)
9. boq_pdf (Attach, Label: BOQ PDF)

Auto Name: SR-.####
```

#### Quote Response DocType
```
Name: Quote Response
Module: threequotes
Fields:
1. service_request (Link, Label: Service Request, Options: Service Request)
2. vendor (Link, Label: Vendor, Options: Vendor)
3. quote_amount (Currency, Label: Quote Amount)
4. quote_details (Text Editor, Label: Quote Details)
5. response_date (Date, Label: Response Date, Default: Today)
6. status (Select, Label: Status, Options: Pending\nSubmitted\nAccepted\nRejected, Default: Pending)
7. attachment (Attach, Label: Attachment)
```

#### BOQ Template DocType
```
Name: BOQ Template
Module: threequotes
Fields:
1. category (Link, Label: Category, Options: Service Category)
2. template_name (Data, Label: Template Name)
3. template_content (Long Text, Label: Template Content)
4. variables (Small Text, Label: Variables (JSON))
```

### 4. Sample Data Setup Commands

```bash
# Access python console
bench --site your-site.localhost console

# Create sample service categories
from frappe import get_doc

# Printing Category
printing = get_doc({
    "doctype": "Service Category",
    "category_name": "Printing",
    "description": "Printing and design services",
    "ai_prompt_template": "What type of printing do you need? How many copies? What size?",
    "status": "Active"
})
printing.insert()

# Accounting Category
accounting = get_doc({
    "doctype": "Service Category", 
    "category_name": "Accounting",
    "description": "Accounting and bookkeeping services",
    "ai_prompt_template": "What accounting services do you need? Monthly/yearly? Number of transactions?",
    "status": "Active"
})
accounting.insert()

# Digital Marketing Category
marketing = get_doc({
    "doctype": "Service Category",
    "category_name": "Digital Marketing", 
    "description": "Digital marketing and advertising",
    "ai_prompt_template": "What marketing services do you need? Social media? SEO? PPC?",
    "status": "Active"
})
marketing.insert()

# Commit changes
frappe.db.commit()
```

### 5. Create Basic Web Pages

#### Create index.html
```bash
# Create templates directory
mkdir -p threequotes/templates/pages

# Create index.html
cat > threequotes/templates/pages/index.html << 'EOF'
{% extends "templates/web.html" %}

{% block title %}3kwotes - Get Business Service Quotes{% endblock %}

{% block page_content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-10">
            <div class="text-center py-5">
                <h1 class="display-4">Get Multiple Quotes for Your Business Services</h1>
                <p class="lead">Submit your requirements and receive competitive quotes from verified vendors</p>
                <a href="/request" class="btn btn-primary btn-lg">Get Quotes Now</a>
            </div>
            
            <div class="row mt-5">
                <div class="col-md-4 text-center">
                    <h3>Printing</h3>
                    <p>Business cards, brochures, banners</p>
                </div>
                <div class="col-md-4 text-center">
                    <h3>Accounting</h3>
                    <p>Bookkeeping, tax filing, auditing</p>
                </div>
                <div class="col-md-4 text-center">
                    <h3>Digital Marketing</h3>
                    <p>SEO, social media, PPC advertising</p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
EOF
```

### 6. Essential Hooks Configuration

```bash
# Edit hooks.py
cat >> threequotes/hooks.py << 'EOF'

# Web pages
web_include_css = [
    "assets/css/threequotes.css"
]

web_include_js = [
    "assets/js/threequotes.js"
]

# Website route rules
website_route_rules = [
    {"from_route": "/", "to_route": "index"},
    {"from_route": "/request", "to_route": "request"},
    {"from_route": "/vendor", "to_route": "vendor"}
]
EOF
```

### 7. Build and Test

```bash
# Build the app
bench build --app threequotes

# Clear cache
bench --site your-site.localhost clear-cache

# Test access
curl http://your-site.localhost:8000/
```

## Fast Development Tips

### 1. Use ERPNext Patterns
```bash
# Copy Customer doctype structure
cp apps/erpnext/erpnext/selling/doctype/customer/customer.py threequotes/threequotes/doctype/vendor/vendor.py

# Copy Quotation workflow
cp apps/erpnext/erpnext/selling/doctype/quotation/quotation.py threequotes/threequotes/doctype/service_request/service_request.py
```

### 2. Quick Email Setup
```bash
# Add to site config
echo '{"mail_server": "smtp.gmail.com", "mail_port": 587, "use_tls": 1, "mail_login": "your-email@gmail.com", "mail_password": "your-password"}' > sites/your-site.localhost/site_config.json
```

### 3. Rapid Testing
```bash
# Quick test script
cat > test_flow.py << 'EOF'
import frappe

# Test service request creation
sr = frappe.get_doc({
    "doctype": "Service Request",
    "customer_name": "Test Customer",
    "customer_email": "test@example.com",
    "service_category": "Printing",
    "status": "Draft"
})
sr.insert()
print(f"Created: {sr.name}")
EOF

bench --site your-site.localhost console < test_flow.py
```

## Common Issues & Quick Fixes

### 1. DocType Not Showing
```bash
bench --site your-site.localhost clear-cache
bench --site your-site.localhost migrate
```

### 2. Web Page Not Loading
```bash
bench build --app threequotes
bench --site your-site.localhost clear-website-cache
```

### 3. Email Not Sending
```bash
# Check email queue
bench --site your-site.localhost console
>>> frappe.get_all("Email Queue")
```

### 4. Static Files Not Loading
```bash
# Rebuild assets
bench build
# Or for development
bench watch
```

## Time-Saving Code Snippets

### Service Request Controller Template
```python
import frappe
from frappe.model.document import Document

class ServiceRequest(Document):
    def before_save(self):
        if not self.created_date:
            self.created_date = frappe.utils.today()
    
    def on_submit(self):
        self.send_to_vendors()
        self.status = "Sent to Vendors"
    
    def send_to_vendors(self):
        # Get vendors for this category
        vendors = frappe.get_all("Vendor", 
            filters={"status": "Active"}, 
            fields=["name", "email"])
        
        for vendor in vendors:
            frappe.sendmail(
                recipients=[vendor.email],
                subject=f"New BOQ Request - {self.service_category}",
                message=f"Please find attached BOQ for {self.name}",
                attachments=[{
                    "fname": f"{self.name}.pdf",
                    "fcontent": self.boq_generated
                }]
            )
```

### Web Form Template
```html
<!-- request.html -->
{% extends "templates/web.html" %}

{% block page_content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <h2>Request Service Quote</h2>
            <form method="post" action="/api/method/threequotes.api.submit_request">
                <div class="form-group">
                    <label>Service Category</label>
                    <select class="form-control" name="service_category" required>
                        <option value="">Select Category</option>
                        {% for category in frappe.get_all("Service Category", filters={"status": "Active"}) %}
                        <option value="{{ category.name }}">{{ category.name }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="form-group">
                    <label>Your Name</label>
                    <input type="text" class="form-control" name="customer_name" required>
                </div>
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" class="form-control" name="customer_email" required>
                </div>
                <button type="submit" class="btn btn-primary">Submit Request</button>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

---

**Remember**: This is a rapid MVP development. Focus on getting the core functionality working first, then add polish and features incrementally. 
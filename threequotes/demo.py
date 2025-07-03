#!/usr/bin/env python3
"""
Demo Data Setup for 3kwotes - Following ERPNext Pattern
Execute using: bench --site your-site execute threequotes.demo.setup_demo_data
"""

import frappe
from frappe.utils import today, add_days

def setup_demo_data():
    """Main function to create demo data for 3kwotes testing"""
    
    print("Setting up demo data for 3kwotes...")
    
    # Create sample service categories first
    create_service_categories()
    
    # Create sample vendors
    create_sample_vendors()
    
    # Create sample BOQ templates
    create_boq_templates()
    
    # Create sample service requests
    create_sample_service_requests()
    
    print("Demo data setup completed!")
    
    # Commit the changes
    frappe.db.commit()
    
    print("All changes committed to database!")

def create_service_categories():
    """Create sample service categories"""
    
    categories = [
        {
            "category_name": "Printing",
            "description": "Business cards, brochures, flyers, and other printing services",
            "status": "Active",
            "icon": "fa-print"
        },
        {
            "category_name": "Accounting",
            "description": "Bookkeeping, tax preparation, and financial services",
            "status": "Active",
            "icon": "fa-calculator"
        },
        {
            "category_name": "Digital Marketing",
            "description": "Social media management, SEO, and online advertising",
            "status": "Active",
            "icon": "fa-bullhorn"
        }
    ]
    
    for cat_data in categories:
        if not frappe.db.exists("Service Category", cat_data["category_name"]):
            category = frappe.new_doc("Service Category")
            category.update(cat_data)
            category.insert()
            print(f"Created service category: {category.category_name}")
        else:
            print(f"Service category already exists: {cat_data['category_name']}")

def create_boq_templates():
    """Create sample BOQ templates"""
    
    templates = [
        {
            "service_category": "Printing",
            "template_name": "Standard Printing BOQ",
            "template_content": """
**PRINTING SERVICE QUOTATION**

Based on your requirements: {chat_transcript}

**RECOMMENDED SOLUTION:**
- Material: Premium quality paper/cardstock
- Printing: High-resolution digital/offset printing
- Finishing: Professional cutting and finishing
- Delivery: Standard packaging and delivery

**ITEMS TO QUOTE:**
1. Design and pre-press work
2. Paper/material cost
3. Printing charges (per unit)
4. Finishing and binding
5. Delivery charges

**TIMELINE:** 3-5 business days
**WARRANTY:** Quality guarantee on all prints

Please provide your detailed quotation for the above requirements.
            """,
            "variables": '["chat_transcript"]'
        },
        {
            "service_category": "Accounting",
            "template_name": "Standard Accounting BOQ",
            "template_content": """
**ACCOUNTING SERVICE QUOTATION**

Based on your requirements: {chat_transcript}

**RECOMMENDED SOLUTION:**
- Monthly bookkeeping and reconciliation
- Financial statements preparation
- Tax compliance and filing
- GST returns and compliance

**SERVICES TO QUOTE:**
1. Monthly bookkeeping (per month)
2. Financial statements preparation
3. Tax return filing
4. GST compliance
5. Additional consultation hours

**TIMELINE:** Ongoing monthly service
**COMPLIANCE:** All statutory requirements included

Please provide your detailed quotation for the above services.
            """,
            "variables": '["chat_transcript"]'
        },
        {
            "service_category": "Digital Marketing",
            "template_name": "Standard Digital Marketing BOQ",
            "template_content": """
**DIGITAL MARKETING SERVICE QUOTATION**

Based on your requirements: {chat_transcript}

**RECOMMENDED SOLUTION:**
- Social media strategy and content creation
- Search engine optimization (SEO)
- Online advertising campaigns
- Performance tracking and reporting

**SERVICES TO QUOTE:**
1. Social media management (per month)
2. Content creation and design
3. SEO optimization
4. Paid advertising management
5. Monthly reporting and analytics

**TIMELINE:** 3-month minimum engagement
**DELIVERABLES:** Monthly reports and performance metrics

Please provide your detailed quotation for the above services.
            """,
            "variables": '["chat_transcript"]'
        }
    ]
    
    for template_data in templates:
        template_name = f"{template_data['service_category']} - {template_data['template_name']}"
        if not frappe.db.exists("BOQ Template", template_name):
            template = frappe.new_doc("BOQ Template")
            template.update(template_data)
            template.insert()
            print(f"Created BOQ template: {template_name}")
        else:
            print(f"BOQ template already exists: {template_name}")

def create_sample_vendors():
    """Create sample vendors for testing"""
    
    vendors_data = [
        {
            "vendor_name": "PrintPro Solutions",
            "email": "contact@printpro.com",
            "phone": "9876543210",
            "service_categories": ["Printing"],
            "rating": 4,
            "response_time": 12
        },
        {
            "vendor_name": "QuickPrint Services",
            "email": "info@quickprint.com", 
            "phone": "9876543211",
            "service_categories": ["Printing"],
            "rating": 5,
            "response_time": 8
        },
        {
            "vendor_name": "Accurate Accounting",
            "email": "services@accurate.com",
            "phone": "9876543212", 
            "service_categories": ["Accounting"],
            "rating": 4,
            "response_time": 24
        },
        {
            "vendor_name": "TaxPro Consultants",
            "email": "hello@taxpro.com",
            "phone": "9876543213",
            "service_categories": ["Accounting"],
            "rating": 5,
            "response_time": 16
        },
        {
            "vendor_name": "DigitalBoost Marketing",
            "email": "team@digitalboost.com",
            "phone": "9876543214",
            "service_categories": ["Digital Marketing"],
            "rating": 4,
            "response_time": 20
        },
        {
            "vendor_name": "SocialMedia Experts",
            "email": "contact@socialmedia.com",
            "phone": "9876543215",
            "service_categories": ["Digital Marketing"],
            "rating": 3,
            "response_time": 48
        }
    ]
    
    for vendor_data in vendors_data:
        if not frappe.db.exists("Vendor", {"email": vendor_data["email"]}):
            vendor = frappe.new_doc("Vendor")
            vendor.vendor_name = vendor_data["vendor_name"]
            vendor.email = vendor_data["email"]
            vendor.phone = vendor_data["phone"]
            vendor.rating = vendor_data["rating"]
            vendor.response_time = vendor_data["response_time"]
            vendor.status = "Active"
            
            # Add service categories
            for category in vendor_data["service_categories"]:
                vendor.append("service_categories", {
                    "service_category": category
                })
            
            vendor.insert()
            print(f"Created vendor: {vendor.vendor_name}")
        else:
            print(f"Vendor already exists: {vendor_data['vendor_name']}")

def create_sample_service_requests():
    """Create sample service requests for testing"""
    
    requests_data = [
        {
            "customer_name": "John Smith",
            "customer_email": "john@example.com", 
            "customer_phone": "9876543220",
            "service_category": "Printing",
            "chat_transcript": """I need 1000 business cards printed with the following specifications:
- Size: Standard 3.5" x 2"
- Paper: Premium matte finish
- Colors: Full color both sides
- Include company logo and contact details
- Timeline: Need within 1 week
- Budget: Around ₹5,000"""
        },
        {
            "customer_name": "Sarah Johnson",
            "customer_email": "sarah@company.com",
            "customer_phone": "9876543221", 
            "service_category": "Accounting",
            "chat_transcript": """I need bookkeeping services for my small business:
- Monthly financial statements
- Tax preparation and filing
- GST returns
- Around 50 transactions per month
- Need services starting next month
- Budget: ₹10,000 per month"""
        },
        {
            "customer_name": "Mike Wilson", 
            "customer_email": "mike@startup.com",
            "customer_phone": "9876543222",
            "service_category": "Digital Marketing",
            "chat_transcript": """Looking for digital marketing services for my startup:
- Social media management (Facebook, Instagram, LinkedIn)
- SEO for website
- Google Ads campaign
- Content creation
- 3 month contract
- Budget: ₹25,000 per month"""
        },
        {
            "customer_name": "Lisa Brown",
            "customer_email": "lisa@restaurant.com", 
            "customer_phone": "9876543223",
            "service_category": "Printing",
            "chat_transcript": """Need menu printing for my restaurant:
- 500 copies of 4-page menu
- A4 size, folded to A5
- High-quality paper with lamination
- Full color printing
- Need within 3 days
- Budget: ₹15,000"""
        }
    ]
    
    for req_data in requests_data:
        if not frappe.db.exists("Service Request", {"customer_email": req_data["customer_email"], "service_category": req_data["service_category"]}):
            service_request = frappe.new_doc("Service Request")
            service_request.customer_name = req_data["customer_name"]
            service_request.customer_email = req_data["customer_email"]
            service_request.customer_phone = req_data["customer_phone"]
            service_request.service_category = req_data["service_category"]
            service_request.chat_transcript = req_data["chat_transcript"]
            service_request.created_date = today()
            
            service_request.insert()
            print(f"Created service request: {service_request.name}")
            
            # Submit the request to trigger BOQ generation
            try:
                service_request.submit()
                print(f"Submitted service request: {service_request.name}")
            except Exception as e:
                print(f"Error submitting service request {service_request.name}: {str(e)}")
        else:
            print(f"Service request already exists for: {req_data['customer_name']}")

# For ERPNext compatibility - this is the standard pattern
if __name__ == "__main__":
    setup_demo_data() 
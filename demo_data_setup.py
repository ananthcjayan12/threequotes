#!/usr/bin/env python3
"""
Demo Data Setup Script for 3kwotes
Run this script in bench console to create sample data for testing
"""

import frappe
from frappe.utils import today, add_days

def setup_demo_data():
    """Create demo data for 3kwotes testing"""
    
    print("Setting up demo data for 3kwotes...")
    
    # Create sample vendors
    create_sample_vendors()
    
    # Create sample service requests
    create_sample_service_requests()
    
    print("Demo data setup completed!")

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
        # Check if vendor already exists
        if not frappe.db.exists("Vendor", {"email": vendor_data["email"]}):
            # Create vendor
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
        # Check if request already exists
        if not frappe.db.exists("Service Request", {"customer_email": req_data["customer_email"], "service_category": req_data["service_category"]}):
            # Create service request
            service_request = frappe.new_doc("Service Request")
            service_request.customer_name = req_data["customer_name"]
            service_request.customer_email = req_data["customer_email"]
            service_request.customer_phone = req_data["customer_phone"]
            service_request.service_category = req_data["service_category"]
            service_request.chat_transcript = req_data["chat_transcript"]
            service_request.created_date = today()
            
            service_request.insert()
            print(f"Created service request: {service_request.name}")
            
            # Submit the request to trigger BOQ generation and vendor dispatch
            service_request.submit()
            print(f"Submitted service request: {service_request.name}")
            
        else:
            print(f"Service request already exists for: {req_data['customer_name']}")

# Usage instructions
if __name__ == "__main__":
    print("""
    To run this script:
    
    1. Open bench console:
       bench --site your-site console
    
    2. Run the script:
       exec(open('demo_data_setup.py').read())
       
    Or run the function directly:
       setup_demo_data()
    """)
else:
    # When imported, run automatically
    setup_demo_data() 
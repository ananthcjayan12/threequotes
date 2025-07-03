#!/usr/bin/env python3
"""
3kwotes MVP Quick Setup Script
Run this script in Frappe console to create sample data and test the system

Usage:
bench --site your-site.localhost console
>>> exec(open('quick_setup_script.py').read())
"""

import frappe

def setup_3kwotes_sample_data():
    """Create sample data for 3kwotes MVP"""
    
    print("🚀 Setting up 3kwotes sample data...")
    
    # 1. Create Service Categories
    categories = [
        {
            "category_name": "Printing",
            "description": "Printing and design services including business cards, brochures, banners",
            "ai_prompt_template": "What type of printing do you need? How many copies? What size and format? Any specific design requirements?",
            "status": "Active",
            "icon": "fa fa-print"
        },
        {
            "category_name": "Accounting", 
            "description": "Accounting and bookkeeping services for businesses",
            "ai_prompt_template": "What accounting services do you need? Monthly/yearly? Number of transactions? Business type?",
            "status": "Active",
            "icon": "fa fa-calculator"
        },
        {
            "category_name": "Digital Marketing",
            "description": "Digital marketing and advertising services",
            "ai_prompt_template": "What marketing services do you need? Social media? SEO? PPC advertising? Target audience?",
            "status": "Active", 
            "icon": "fa fa-bullhorn"
        }
    ]
    
    created_categories = []
    for cat_data in categories:
        if not frappe.db.exists("Service Category", cat_data["category_name"]):
            category = frappe.get_doc({
                "doctype": "Service Category",
                **cat_data
            })
            category.insert()
            created_categories.append(category.name)
            print(f"✅ Created Service Category: {category.name}")
        else:
            print(f"⚠️  Service Category already exists: {cat_data['category_name']}")
    
    # 2. Create BOQ Templates
    templates = [
        {
            "category": "Printing",
            "template_name": "Standard Printing Template",
            "template_content": """
            <h4>Printing Services Quote</h4>
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="background: #f8f9fa;">
                    <th style="border: 1px solid #ddd; padding: 8px;">Item</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">Quantity</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">Specifications</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">Est. Unit Price</th>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;">Business Cards</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">1000 pcs</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">Standard size, both sides</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">$0.10 per card</td>
                </tr>
            </table>
            """,
            "variables": '{"quantity": "1000", "item_type": "Business Cards", "specifications": "Standard"}'
        },
        {
            "category": "Accounting",
            "template_name": "Monthly Accounting Template", 
            "template_content": """
            <h4>Monthly Accounting Services</h4>
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="background: #f8f9fa;">
                    <th style="border: 1px solid #ddd; padding: 8px;">Service</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">Frequency</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">Scope</th>
                </tr>
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;">Bookkeeping</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">Monthly</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">Up to 100 transactions</td>
                </tr>
            </table>
            """,
            "variables": '{"frequency": "Monthly", "transaction_limit": "100"}'
        }
    ]
    
    for template_data in templates:
        if not frappe.db.exists("BOQ Template", {"category": template_data["category"], "template_name": template_data["template_name"]}):
            template = frappe.get_doc({
                "doctype": "BOQ Template",
                **template_data
            })
            template.insert()
            print(f"✅ Created BOQ Template: {template.template_name}")
    
    # 3. Create Sample Vendors
    vendors = [
        {
            "vendor_name": "PrintPro Solutions",
            "email": "contact@printpro.com",
            "phone": "+1-555-0101",
            "status": "Active",
            "rating": 4,
            "response_time": 12,
            "service_categories": [{"service_category": "Printing"}]
        },
        {
            "vendor_name": "QuickPrint Services", 
            "email": "orders@quickprint.com",
            "phone": "+1-555-0102",
            "status": "Active",
            "rating": 5,
            "response_time": 24,
            "service_categories": [{"service_category": "Printing"}]
        },
        {
            "vendor_name": "Digital Print Hub",
            "email": "hello@digitalprinthub.com", 
            "phone": "+1-555-0103",
            "status": "Active",
            "rating": 3,
            "response_time": 18,
            "service_categories": [{"service_category": "Printing"}]
        },
        {
            "vendor_name": "AccountPro Services",
            "email": "info@accountpro.com",
            "phone": "+1-555-0201", 
            "status": "Active",
            "rating": 5,
            "response_time": 24,
            "service_categories": [{"service_category": "Accounting"}]
        },
        {
            "vendor_name": "BookKeeping Plus",
            "email": "contact@bookkeepingplus.com",
            "phone": "+1-555-0202",
            "status": "Active", 
            "rating": 4,
            "response_time": 48,
            "service_categories": [{"service_category": "Accounting"}]
        },
        {
            "vendor_name": "DigitalGrow Marketing",
            "email": "team@digitalgrow.com",
            "phone": "+1-555-0301",
            "status": "Active",
            "rating": 4,
            "response_time": 24,
            "service_categories": [{"service_category": "Digital Marketing"}]
        }
    ]
    
    created_vendors = []
    for vendor_data in vendors:
        if not frappe.db.exists("Vendor", vendor_data["vendor_name"]):
            vendor = frappe.get_doc({
                "doctype": "Vendor",
                **vendor_data
            })
            vendor.insert()
            created_vendors.append(vendor.name)
            print(f"✅ Created Vendor: {vendor.vendor_name}")
        else:
            print(f"⚠️  Vendor already exists: {vendor_data['vendor_name']}")
    
    # 4. Create a Test Service Request
    test_request_data = {
        "doctype": "Service Request",
        "customer_name": "John Doe",
        "customer_email": "john.doe@example.com",
        "customer_phone": "+1-555-9999",
        "service_category": "Printing",
        "chat_transcript": """
        Customer: Hi, I need business cards for my new company
        Agent: Great! How many cards do you need?
        Customer: I need 1000 business cards
        Agent: What specifications do you need?
        Customer: Standard size, double-sided, with logo and contact info
        Agent: Any specific design requirements?
        Customer: Professional design, blue and white color scheme
        """
    }
    
    if not frappe.db.exists("Service Request", {"customer_email": test_request_data["customer_email"]}):
        service_request = frappe.get_doc(test_request_data)
        service_request.insert()
        print(f"✅ Created Test Service Request: {service_request.name}")
        
        # BOQ should be auto-generated
        if service_request.boq_generated:
            print(f"✅ BOQ auto-generated successfully")
        else:
            print(f"⚠️  BOQ was not generated automatically")
            
        return service_request.name
    else:
        print(f"⚠️  Test service request already exists")
        return None

def test_workflow():
    """Test the complete workflow"""
    print("\n🧪 Testing 3kwotes Workflow...")
    
    # Find a test service request
    test_request = frappe.get_value("Service Request", {"customer_name": "John Doe"})
    
    if not test_request:
        print("❌ No test service request found")
        return
    
    service_request = frappe.get_doc("Service Request", test_request)
    
    print(f"📋 Testing Service Request: {service_request.name}")
    print(f"   Customer: {service_request.customer_name}")
    print(f"   Category: {service_request.service_category}")
    print(f"   Status: {service_request.status}")
    print(f"   BOQ Generated: {'✅ Yes' if service_request.boq_generated else '❌ No'}")
    
    # Test vendor matching
    if service_request.service_category:
        vendors = frappe.get_all("Vendor", 
            filters={"status": "Active"},
            fields=["name", "vendor_name", "email"])
        
        relevant_vendors = []
        for vendor in vendors:
            vendor_doc = frappe.get_doc("Vendor", vendor.name)
            if vendor_doc.can_handle_category(service_request.service_category):
                relevant_vendors.append(vendor_doc)
        
        print(f"🏪 Found {len(relevant_vendors)} vendors for {service_request.service_category}:")
        for vendor in relevant_vendors:
            print(f"   - {vendor.vendor_name} (Rating: {vendor.rating}⭐)")

def show_summary():
    """Show summary of created data"""
    print("\n📊 3kwotes Setup Summary:")
    print("=" * 50)
    
    categories = frappe.get_all("Service Category", fields=["name", "status"])
    print(f"📂 Service Categories: {len(categories)}")
    for cat in categories:
        print(f"   - {cat.name} ({cat.status})")
    
    vendors = frappe.get_all("Vendor", fields=["vendor_name", "status", "rating"])
    print(f"\n🏪 Vendors: {len(vendors)}")
    for vendor in vendors:
        print(f"   - {vendor.vendor_name} ({vendor.rating}⭐, {vendor.status})")
    
    templates = frappe.get_all("BOQ Template", fields=["template_name", "category"])
    print(f"\n📝 BOQ Templates: {len(templates)}")
    for template in templates:
        print(f"   - {template.template_name} ({template.category})")
    
    requests = frappe.get_all("Service Request", fields=["name", "customer_name", "status"])
    print(f"\n📋 Service Requests: {len(requests)}")
    for request in requests:
        print(f"   - {request.name}: {request.customer_name} ({request.status})")
    
    print("\n🎉 Setup Complete! Your 3kwotes MVP backend is ready!")
    print("\nNext Steps:")
    print("1. Test the workflow by creating more service requests")
    print("2. Configure email settings for notifications")
    print("3. Create web interface (Phase 3 of development guide)")
    print("4. Add vendor portal (Phase 4)")
    print("5. Polish and deploy (Phase 5)")

# Main execution
if __name__ == "__main__":
    try:
        # Set administrator as current user for permissions
        frappe.set_user("Administrator")
        
        # Run setup
        setup_3kwotes_sample_data()
        test_workflow()
        show_summary()
        
        # Commit changes
        frappe.db.commit()
        
    except Exception as e:
        print(f"❌ Error during setup: {str(e)}")
        frappe.db.rollback()
        raise 
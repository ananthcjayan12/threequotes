import frappe
from frappe import _

def get_context(context):
	"""Get context data for admin dashboard page"""
	
	# Check if user is admin
	context.is_admin = is_admin_user()
	
	if context.is_admin:
		# Get dashboard statistics
		context.stats = get_dashboard_stats()
		
		# Get recent service requests
		context.service_requests = get_recent_service_requests()
		
		# Get service categories
		context.service_categories = get_service_categories()
		
		# Get vendors
		context.vendors = get_vendors()
	
	# Set meta tags
	context.title = "Admin Dashboard - 3kwotes"
	context.description = "Admin dashboard for managing service requests, vendors, and system performance."
	
	return context

def is_admin_user():
	"""Check if current user is admin"""
	if frappe.session.user in ["Administrator", "admin@3kwotes.com"]:
		return True
	
	# Check if user has System Manager role
	user_roles = frappe.get_roles(frappe.session.user)
	return "System Manager" in user_roles

def get_dashboard_stats():
	"""Get dashboard statistics"""
	try:
		stats = {}
		
		# Total service requests
		stats['total_requests'] = frappe.db.count("Service Request")
		
		# Active vendors
		stats['active_vendors'] = frappe.db.count("Vendor", {"status": "Active"})
		
		# Total quotes
		stats['total_quotes'] = frappe.db.count("Quote Response")
		
		# Service categories
		stats['service_categories'] = frappe.db.count("Service Category", {"status": "Active"})
		
		return stats
		
	except Exception as e:
		frappe.log_error(f"Error getting dashboard stats: {str(e)}")
		return {
			'total_requests': 0,
			'active_vendors': 0,
			'total_quotes': 0,
			'service_categories': 0
		}

def get_recent_service_requests(limit=10):
	"""Get recent service requests"""
	try:
		requests = frappe.db.sql("""
			SELECT 
				sr.name,
				sr.customer_name,
				sr.customer_email,
				sr.customer_phone,
				sr.chat_transcript,
				sr.status,
				sr.creation,
				sc.category_name as service_category_name
			FROM 
				`tabService Request` sr
				LEFT JOIN `tabService Category` sc ON sr.service_category = sc.name
			ORDER BY 
				sr.creation DESC
			LIMIT %s
		""", (limit,), as_dict=True)
		
		return requests
		
	except Exception as e:
		frappe.log_error(f"Error getting recent service requests: {str(e)}")
		return []

def get_service_categories():
	"""Get all service categories"""
	try:
		categories = frappe.get_all("Service Category",
			fields=["name", "category_name", "description", "status", "icon"],
			order_by="category_name"
		)
		
		# Add request counts for each category
		for category in categories:
			category['requests_count'] = frappe.db.count("Service Request", 
				{"service_category": category.name})
			category['vendors_count'] = frappe.db.count("Vendor Service Category", 
				{"service_category": category.name})
		
		return categories
		
	except Exception as e:
		frappe.log_error(f"Error getting service categories: {str(e)}")
		return []

def get_vendors(limit=20):
	"""Get vendors with basic stats"""
	try:
		vendors = frappe.db.sql("""
			SELECT 
				v.name,
				v.vendor_name,
				v.email,
				v.phone,
				v.status,
				v.rating,
				v.response_time,
				COUNT(vsc.service_category) as service_categories_count
			FROM 
				`tabVendor` v
				LEFT JOIN `tabVendor Service Category` vsc ON v.name = vsc.parent
			GROUP BY 
				v.name
			ORDER BY 
				v.creation DESC
			LIMIT %s
		""", (limit,), as_dict=True)
		
		return vendors
		
	except Exception as e:
		frappe.log_error(f"Error getting vendors: {str(e)}")
		return [] 
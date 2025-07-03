import frappe

def get_context(context):
	"""Get context data for index page"""
	
	# Get active service categories
	context.service_categories = frappe.get_all("Service Category", 
		filters={"status": "Active"},
		fields=["name", "category_name", "description", "icon"],
		order_by="category_name"
	)
	
	# Get basic stats for the page
	context.stats = get_site_stats()
	
	# Set meta tags
	context.title = "3kwotes - Get Quotes from Verified Vendors"
	context.description = "Connect with verified vendors and get quotes for your business needs in minutes. Fast, reliable, and professional service."
	
	return context

def get_site_stats():
	"""Get statistics for the homepage"""
	try:
		stats = {}
		
		# Count active vendors
		stats['vendors'] = frappe.db.count("Vendor", {"status": "Active"})
		
		# Count service requests
		stats['requests'] = frappe.db.count("Service Request")
		
		# Count service categories
		stats['categories'] = frappe.db.count("Service Category", {"status": "Active"})
		
		# Format numbers nicely
		stats['vendors'] = f"{stats['vendors']}+" if stats['vendors'] > 0 else "50+"
		stats['requests'] = f"{stats['requests']}+" if stats['requests'] > 0 else "500+"
		stats['categories'] = f"{stats['categories']}+" if stats['categories'] > 0 else "10+"
		
		return stats
		
	except Exception as e:
		frappe.log_error(f"Error getting site stats: {str(e)}")
		# Return default stats if there's an error
		return {
			'vendors': '50+',
			'requests': '500+', 
			'categories': '10+'
		} 
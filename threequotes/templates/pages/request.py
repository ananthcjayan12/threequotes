import frappe

def get_context(context):
	"""Get context data for request page"""
	
	# Get active service categories
	context.service_categories = frappe.get_all("Service Category", 
		filters={"status": "Active"},
		fields=["name", "category_name", "description", "icon", "ai_prompt_template"],
		order_by="category_name"
	)
	
	# Set meta tags
	context.title = "Submit Service Request - 3kwotes"
	context.description = "Submit your service request and get quotes from verified vendors within 24-48 hours."
	
	return context 
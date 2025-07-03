import frappe
from frappe import _
from datetime import datetime, timedelta

def get_context(context):
	"""Get context data for vendor portal page"""
	
	# Get current user - following Frappe's pattern
	if frappe.session.user != "Guest":
		context.current_user = frappe.get_doc("User", frappe.session.user)
		context.user = context.current_user  # For template compatibility
		
		# Try to find vendor record for current user
		vendor = get_vendor_by_user(frappe.session.user)
		if vendor:
			context.vendor = vendor
			context.boq_assignments = get_vendor_boq_assignments(vendor.name)
			context.stats = get_vendor_stats(vendor.name)
		else:
			# User is logged in but not a vendor
			context.vendor = None
			context.boq_assignments = []
			context.stats = {}
	else:
		context.user = None
		context.vendor = None
		context.boq_assignments = []
		context.stats = {}
	
	# Set meta tags
	context.title = "Vendor Portal - 3kwotes"
	context.description = "Access your BOQ assignments and submit quotes to customers."
	
	return context

def get_vendor_by_user(user_email):
	"""Get vendor record by user email"""
	try:
		vendor_name = frappe.db.get_value("Vendor", {"email": user_email}, "name")
		if vendor_name:
			return frappe.get_doc("Vendor", vendor_name)
		return None
	except:
		return None

def get_vendor_boq_assignments(vendor_name):
	"""Get BOQ assignments for a vendor"""
	try:
		# Get vendor's service categories
		vendor_categories = frappe.get_all("Vendor Service Category", 
			filters={"parent": vendor_name},
			fields=["service_category"]
		)
		
		if not vendor_categories:
			return []
		
		category_names = [cat.service_category for cat in vendor_categories]
		
		# Get service requests for vendor's categories
		assignments = frappe.db.sql("""
			SELECT 
				sr.name as request_id,
				sr.customer_name,
				sr.customer_email,
				sr.chat_transcript,
				sr.boq_generated,
				sr.status,
				sr.creation as created_date,
				sc.category_name as service_category_name,
				COALESCE(qr.quote_amount, 0) as quote_amount,
				COALESCE(qr.status, 'Pending') as quote_status,
				CASE 
					WHEN DATEDIFF(NOW(), sr.creation) > 2 THEN 'high'
					WHEN DATEDIFF(NOW(), sr.creation) > 1 THEN 'medium'
					ELSE 'low'
				END as urgency
			FROM 
				`tabService Request` sr
				LEFT JOIN `tabService Category` sc ON sr.service_category = sc.name
				LEFT JOIN `tabQuote Response` qr ON sr.name = qr.service_request AND qr.vendor = %s
			WHERE 
				sr.service_category IN ({})
				AND sr.status IN ('BOQ Generated', 'Sent to Vendors', 'Quotes Received')
				AND sr.docstatus = 1
			ORDER BY 
				sr.creation DESC
		""".format(','.join(['%s'] * len(category_names))), 
		tuple([vendor_name] + category_names), as_dict=True)
		
		# Format the data
		for assignment in assignments:
			assignment.status = assignment.quote_status if assignment.quote_status != 'Pending' else 'Pending'
			assignment.created_date = assignment.created_date.strftime('%d %b %Y') if assignment.created_date else ''
			
		return assignments
		
	except Exception as e:
		frappe.log_error(f"Error getting vendor BOQ assignments: {str(e)}")
		return []

def get_vendor_stats(vendor_name):
	"""Get vendor statistics"""
	try:
		stats = {}
		
		# Get total quotes submitted
		stats['submitted_quotes'] = frappe.db.count("Quote Response", {"vendor": vendor_name})
		
		# Get pending BOQs count (assignments without quotes)
		vendor_categories = frappe.get_all("Vendor Service Category", 
			filters={"parent": vendor_name},
			fields=["service_category"]
		)
		
		if vendor_categories:
			category_names = [cat.service_category for cat in vendor_categories]
			
			# Count pending BOQs
			pending_boqs = frappe.db.sql("""
				SELECT COUNT(*) as count
				FROM `tabService Request` sr
				WHERE sr.service_category IN ({})
				AND sr.status IN ('BOQ Generated', 'Sent to Vendors')
				AND sr.name NOT IN (
					SELECT service_request 
					FROM `tabQuote Response` 
					WHERE vendor = %s
				)
			""".format(','.join(['%s'] * len(category_names))), 
			tuple(category_names + [vendor_name]))[0][0]
			
			stats['pending_boqs'] = pending_boqs
		else:
			stats['pending_boqs'] = 0
		
		# Calculate response rate
		total_assignments = stats['submitted_quotes'] + stats['pending_boqs']
		if total_assignments > 0:
			stats['response_rate'] = round((stats['submitted_quotes'] / total_assignments) * 100)
		else:
			stats['response_rate'] = 0
		
		return stats
		
	except Exception as e:
		frappe.log_error(f"Error getting vendor stats: {str(e)}")
		return {
			'submitted_quotes': 0,
			'pending_boqs': 0,
			'response_rate': 0
		} 
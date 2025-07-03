# Copyright (c) 2025, ananthuuuu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import validate_email_address


class Vendor(Document):
	def validate(self):
		"""Validate the vendor before saving"""
		self.validate_email()
		self.validate_service_categories()
		self.set_default_values()
	
	def validate_email(self):
		"""Validate email format"""
		if self.email:
			validate_email_address(self.email, throw=True)
	
	def validate_service_categories(self):
		"""Ensure at least one service category is selected"""
		if not self.service_categories:
			frappe.throw("Please select at least one service category")
		
		# Check for duplicate service categories
		categories = [row.service_category for row in self.service_categories]
		if len(categories) != len(set(categories)):
			frappe.throw("Duplicate service categories are not allowed")
	
	def set_default_values(self):
		"""Set default values if not provided"""
		if not self.status:
			self.status = "Active"
		
		if not self.rating:
			self.rating = 3  # Default rating
		
		if not self.response_time:
			self.response_time = 24  # Default 24 hours
	
	def before_save(self):
		"""Before save validations"""
		if self.vendor_name:
			# Ensure vendor name is properly formatted
			self.vendor_name = self.vendor_name.strip().title()
	
	def get_service_categories_list(self):
		"""Get list of service categories for this vendor"""
		return [row.service_category for row in self.service_categories]
	
	def can_handle_category(self, category):
		"""Check if vendor can handle a specific service category"""
		if self.status != "Active":
			return False
		
		categories = self.get_service_categories_list()
		return category in categories
	
	@staticmethod
	def get_vendors_for_category(category):
		"""Get all active vendors for a specific service category"""
		return frappe.db.sql("""
			SELECT v.name, v.vendor_name, v.email, v.phone, v.rating, v.response_time
			FROM `tabVendor` v
			JOIN `tabVendor Service Category` vsc ON v.name = vsc.parent
			WHERE v.status = 'Active' 
			AND vsc.service_category = %s
			ORDER BY v.rating DESC, v.response_time ASC
		""", category, as_dict=True)
	
	def send_boq_email(self, service_request_name, boq_content):
		"""Send BOQ email to vendor"""
		if not self.email:
			return False
		
		try:
			frappe.sendmail(
				recipients=[self.email],
				subject=f"New BOQ Request - {service_request_name}",
				message=f"""
				<p>Dear {self.vendor_name},</p>
				<p>You have received a new BOQ request. Please review the details below and submit your quote.</p>
				<div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0;">
					{boq_content}
				</div>
				<p>Please submit your quote by clicking the link below:</p>
				<p><a href="{frappe.utils.get_url()}/vendor-quote?service_request={service_request_name}&vendor={self.name}" 
				   style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
				   Submit Quote</a></p>
				<p>Best regards,<br>3kwotes Team</p>
				""",
				now=True
			)
			return True
		except Exception as e:
			frappe.log_error(f"Failed to send BOQ email to {self.vendor_name}: {str(e)}")
			return False


# Whitelisted functions for web interface
@frappe.whitelist()
def send_test_email(vendor_id):
	"""Send test email to vendor - called from admin dashboard"""
	try:
		vendor = frappe.get_doc("Vendor", vendor_id)
		vendor.check_permission("read")
		
		if not vendor.email:
			return {"success": False, "message": "Vendor email not found"}
		
		frappe.sendmail(
			recipients=[vendor.email],
			subject="Test Email from 3kwotes",
			message=f"""
			<p>Dear {vendor.vendor_name},</p>
			<p>This is a test email to verify your email configuration with 3kwotes.</p>
			<p>If you receive this email, your email setup is working correctly.</p>
			<p>Best regards,<br>3kwotes Team</p>
			""",
			now=True
		)
		
		return {"success": True, "message": "Test email sent successfully"}
	except Exception as e:
		frappe.log_error(f"Error sending test email: {str(e)}")
		return {"success": False, "message": str(e)} 
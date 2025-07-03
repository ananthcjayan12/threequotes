# Copyright (c) 2025, ananthuuuu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class QuoteResponse(Document):
	def validate(self):
		"""Validate quote response before saving"""
		self.validate_service_request_and_vendor()
		self.validate_quote_amount()
	
	def validate_service_request_and_vendor(self):
		"""Validate service request and vendor combination"""
		if self.service_request and self.vendor:
			# Check if vendor can handle the service category
			service_request = frappe.get_doc("Service Request", self.service_request)
			vendor = frappe.get_doc("Vendor", self.vendor)
			
			if not vendor.can_handle_category(service_request.service_category):
				frappe.throw(f"Vendor {vendor.vendor_name} cannot handle {service_request.service_category} services")
	
	def validate_quote_amount(self):
		"""Validate quote amount is positive"""
		if self.quote_amount and self.quote_amount <= 0:
			frappe.throw("Quote amount must be greater than zero")
	
	def before_save(self):
		"""Before save actions"""
		if not self.response_date:
			self.response_date = frappe.utils.today()
	
	def on_submit(self):
		"""Actions when quote is submitted"""
		self.db_set('status', 'Submitted')
		
		# Update service request status
		self.update_service_request_status()
		
		# Send notification to customer
		self.send_customer_notification()
	
	def update_service_request_status(self):
		"""Update service request status when quote is received"""
		service_request = frappe.get_doc("Service Request", self.service_request)
		service_request.update_quotes_received()
	
	def send_customer_notification(self):
		"""Send notification to customer about new quote"""
		if not self.service_request:
			return
		
		service_request = frappe.get_doc("Service Request", self.service_request)
		vendor = frappe.get_doc("Vendor", self.vendor)
		
		if service_request.customer_email:
			try:
				frappe.sendmail(
					recipients=[service_request.customer_email],
					subject=f"New Quote Received for {self.service_request}",
					message=f"""
					<p>Dear {service_request.customer_name},</p>
					<p>You have received a new quote for your service request.</p>
					<div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0;">
						<h4>{vendor.vendor_name}</h4>
						<p><strong>Quote Amount:</strong> {self.quote_amount}</p>
						<p><strong>Details:</strong> {self.quote_details}</p>
						<p><strong>Vendor Email:</strong> {vendor.email}</p>
						<p><strong>Vendor Phone:</strong> {vendor.phone or 'Not provided'}</p>
					</div>
					<p>You can contact the vendor directly to proceed with the service.</p>
					<p>Best regards,<br>3kwotes Team</p>
					""",
					now=True
				)
			except Exception as e:
				frappe.log_error(f"Failed to send customer notification: {str(e)}")
	
	@staticmethod
	def get_quotes_for_service_request(service_request):
		"""Get all quotes for a service request"""
		return frappe.get_all("Quote Response",
			filters={"service_request": service_request, "docstatus": 1},
			fields=["vendor", "quote_amount", "quote_details", "response_date", "status"],
			order_by="quote_amount ASC") 
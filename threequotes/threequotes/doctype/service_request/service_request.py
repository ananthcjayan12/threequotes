# Copyright (c) 2025, ananthuuuu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import validate_email_address, get_url
import json


class ServiceRequest(Document):
	def validate(self):
		"""Validate the service request before saving"""
		self.validate_email()
		self.validate_service_category()
		self.set_default_values()
	
	def validate_email(self):
		"""Validate customer email format"""
		if self.customer_email:
			validate_email_address(self.customer_email, throw=True)
	
	def validate_service_category(self):
		"""Validate service category exists and is active"""
		if self.service_category:
			category = frappe.get_doc("Service Category", self.service_category)
			if category.status != "Active":
				frappe.throw(f"Service Category '{self.service_category}' is not active")
	
	def set_default_values(self):
		"""Set default values if not provided"""
		if not self.created_date:
			self.created_date = frappe.utils.today()
		
		if not self.status:
			self.status = "Draft"
	
	def before_save(self):
		"""Before save actions"""
		if self.customer_name:
			self.customer_name = self.customer_name.strip().title()
		
		# Generate BOQ if chat transcript exists and BOQ doesn't exist
		if self.chat_transcript and not self.boq_generated:
			self.generate_boq()
	
	def generate_boq(self):
		"""Generate BOQ from chat transcript and service category"""
		if not self.service_category:
			return
		
		# Get BOQ template for this service category
		boq_template = frappe.get_value("BOQ Template", 
			{"category": self.service_category}, 
			["template_content", "variables"], as_dict=True)
		
		if boq_template:
			# Use template to generate BOQ
			self.boq_generated = self.process_boq_template(boq_template)
		else:
			# Generate basic BOQ from chat transcript
			self.boq_generated = self.generate_basic_boq()
		
		# Update status
		if self.boq_generated:
			self.status = "BOQ Generated"
	
	def process_boq_template(self, template_data):
		"""Process BOQ template with variables"""
		template_content = template_data.get("template_content", "")
		variables = template_data.get("variables", "{}")
		
		try:
			# Parse variables if they exist
			template_vars = json.loads(variables) if variables else {}
			
			# Create BOQ content with customer details
			boq_content = f"""
			<div style="border: 1px solid #ddd; padding: 20px; margin: 10px 0;">
				<h3>Bill of Quantities (BOQ)</h3>
				<p><strong>Service Request:</strong> {self.name}</p>
				<p><strong>Customer:</strong> {self.customer_name}</p>
				<p><strong>Email:</strong> {self.customer_email}</p>
				<p><strong>Service Category:</strong> {self.service_category}</p>
				<p><strong>Date:</strong> {self.created_date}</p>
				<hr>
				<div>
					{template_content}
				</div>
				<hr>
				<p><strong>Customer Requirements:</strong></p>
				<div style="background: #f8f9fa; padding: 10px; border-radius: 5px;">
					{self.chat_transcript or 'No specific requirements provided'}
				</div>
			</div>
			"""
			
			return boq_content
			
		except Exception as e:
			frappe.log_error(f"Error processing BOQ template: {str(e)}")
			return self.generate_basic_boq()
	
	def generate_basic_boq(self):
		"""Generate basic BOQ when no template is available"""
		category_templates = {
			"Printing": """
			<h4>Printing Services BOQ</h4>
			<table style="width: 100%; border-collapse: collapse;">
				<tr style="background: #f8f9fa;">
					<th style="border: 1px solid #ddd; padding: 8px;">Item</th>
					<th style="border: 1px solid #ddd; padding: 8px;">Quantity</th>
					<th style="border: 1px solid #ddd; padding: 8px;">Specifications</th>
				</tr>
				<tr>
					<td style="border: 1px solid #ddd; padding: 8px;">Printing Service</td>
					<td style="border: 1px solid #ddd; padding: 8px;">As per requirement</td>
					<td style="border: 1px solid #ddd; padding: 8px;">As discussed with customer</td>
				</tr>
			</table>
			""",
			"Accounting": """
			<h4>Accounting Services BOQ</h4>
			<table style="width: 100%; border-collapse: collapse;">
				<tr style="background: #f8f9fa;">
					<th style="border: 1px solid #ddd; padding: 8px;">Service</th>
					<th style="border: 1px solid #ddd; padding: 8px;">Period</th>
					<th style="border: 1px solid #ddd; padding: 8px;">Details</th>
				</tr>
				<tr>
					<td style="border: 1px solid #ddd; padding: 8px;">Accounting Service</td>
					<td style="border: 1px solid #ddd; padding: 8px;">As per requirement</td>
					<td style="border: 1px solid #ddd; padding: 8px;">As discussed with customer</td>
				</tr>
			</table>
			""",
			"Digital Marketing": """
			<h4>Digital Marketing Services BOQ</h4>
			<table style="width: 100%; border-collapse: collapse;">
				<tr style="background: #f8f9fa;">
					<th style="border: 1px solid #ddd; padding: 8px;">Service</th>
					<th style="border: 1px solid #ddd; padding: 8px;">Duration</th>
					<th style="border: 1px solid #ddd; padding: 8px;">Scope</th>
				</tr>
				<tr>
					<td style="border: 1px solid #ddd; padding: 8px;">Digital Marketing</td>
					<td style="border: 1px solid #ddd; padding: 8px;">As per requirement</td>
					<td style="border: 1px solid #ddd; padding: 8px;">As discussed with customer</td>
				</tr>
			</table>
			"""
		}
		
		template = category_templates.get(self.service_category, """
		<h4>Service BOQ</h4>
		<p>Service details will be provided based on your requirements.</p>
		""")
		
		boq_content = f"""
		<div style="border: 1px solid #ddd; padding: 20px; margin: 10px 0;">
			<h3>Bill of Quantities (BOQ)</h3>
			<p><strong>Service Request:</strong> {self.name}</p>
			<p><strong>Customer:</strong> {self.customer_name}</p>
			<p><strong>Email:</strong> {self.customer_email}</p>
			<p><strong>Service Category:</strong> {self.service_category}</p>
			<p><strong>Date:</strong> {self.created_date}</p>
			<hr>
			{template}
			<hr>
			<p><strong>Customer Requirements:</strong></p>
			<div style="background: #f8f9fa; padding: 10px; border-radius: 5px;">
				{self.chat_transcript or 'No specific requirements provided'}
			</div>
		</div>
		"""
		
		return boq_content
	
	def on_submit(self):
		"""Actions to perform when service request is submitted"""
		# Send BOQ to vendors
		self.send_to_vendors()
		
		# Update status
		self.db_set('status', 'Sent to Vendors')
		
		# Send confirmation email to customer
		self.send_customer_confirmation()
	
	def send_to_vendors(self):
		"""Send BOQ to relevant vendors"""
		if not self.service_category or not self.boq_generated:
			return
		
		# Get vendors for this service category
		vendors = frappe.get_all("Vendor", 
			filters={"status": "Active"},
			fields=["name", "vendor_name", "email"])
		
		# Filter vendors by service category
		relevant_vendors = []
		for vendor in vendors:
			vendor_doc = frappe.get_doc("Vendor", vendor.name)
			if vendor_doc.can_handle_category(self.service_category):
				relevant_vendors.append(vendor)
		
		if not relevant_vendors:
			frappe.msgprint("No active vendors found for this service category")
			return
		
		# Send email to each vendor
		sent_count = 0
		for vendor in relevant_vendors:
			try:
				vendor_doc = frappe.get_doc("Vendor", vendor.name)
				if vendor_doc.send_boq_email(self.name, self.boq_generated):
					sent_count += 1
			except Exception as e:
				frappe.log_error(f"Failed to send BOQ to vendor {vendor.name}: {str(e)}")
		
		# Add a comment about emails sent
		self.add_comment("Info", f"BOQ sent to {sent_count} vendors")
	
	def send_customer_confirmation(self):
		"""Send confirmation email to customer"""
		if not self.customer_email:
			return
		
		try:
			frappe.sendmail(
				recipients=[self.customer_email],
				subject=f"Your Service Request {self.name} has been submitted",
				message=f"""
				<p>Dear {self.customer_name},</p>
				<p>Thank you for submitting your service request. We have sent your requirements to our verified vendors.</p>
				<p><strong>Service Request Details:</strong></p>
				<ul>
					<li><strong>Request ID:</strong> {self.name}</li>
					<li><strong>Service Category:</strong> {self.service_category}</li>
					<li><strong>Date:</strong> {self.created_date}</li>
				</ul>
				<p>You will receive quotes from vendors via email within 24-48 hours.</p>
				<p>You can track your request status at: <a href="{get_url()}/service-request/{self.name}">View Request</a></p>
				<p>Best regards,<br>3kwotes Team</p>
				""",
				now=True
			)
		except Exception as e:
			frappe.log_error(f"Failed to send confirmation email: {str(e)}")
	
	def get_quote_responses(self):
		"""Get all quote responses for this service request"""
		return frappe.get_all("Quote Response",
			filters={"service_request": self.name},
			fields=["vendor", "quote_amount", "quote_details", "status", "response_date"],
			order_by="quote_amount ASC")
	
	def update_quotes_received(self):
		"""Update status when quotes are received"""
		quotes = self.get_quote_responses()
		if quotes:
			self.db_set('status', 'Quotes Received')
			
			# Send notification to customer
			self.send_quotes_notification(quotes)
	
	def send_quotes_notification(self, quotes):
		"""Send notification to customer about received quotes"""
		if not self.customer_email:
			return
		
		quotes_html = ""
		for quote in quotes:
			vendor_name = frappe.get_value("Vendor", quote.vendor, "vendor_name")
			quotes_html += f"""
			<div style="border: 1px solid #ddd; padding: 10px; margin: 10px 0;">
				<h4>{vendor_name}</h4>
				<p><strong>Quote Amount:</strong> {quote.quote_amount}</p>
				<p><strong>Details:</strong> {quote.quote_details}</p>
			</div>
			"""
		
		try:
			frappe.sendmail(
				recipients=[self.customer_email],
				subject=f"Quotes Received for {self.name}",
				message=f"""
				<p>Dear {self.customer_name},</p>
				<p>We have received quotes for your service request. Here are the details:</p>
				{quotes_html}
				<p>Please review the quotes and contact the vendor of your choice directly.</p>
				<p>Best regards,<br>3kwotes Team</p>
				""",
				now=True
			)
		except Exception as e:
			frappe.log_error(f"Failed to send quotes notification: {str(e)}") 
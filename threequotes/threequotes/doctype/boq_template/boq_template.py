# Copyright (c) 2025, ananthuuuu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json


class BOQTemplate(Document):
	def validate(self):
		"""Validate BOQ template before saving"""
		self.validate_category()
		self.validate_variables()
	
	def validate_category(self):
		"""Validate service category exists and is active"""
		if self.category:
			category = frappe.get_doc("Service Category", self.category)
			if category.status != "Active":
				frappe.throw(f"Service Category '{self.category}' is not active")
	
	def validate_variables(self):
		"""Validate JSON variables format"""
		if self.variables:
			try:
				json.loads(self.variables)
			except json.JSONDecodeError:
				frappe.throw("Variables must be valid JSON format")
	
	def before_save(self):
		"""Before save actions"""
		if self.template_name:
			self.template_name = self.template_name.strip()
		
		# Set default template content if empty
		if not self.template_content and self.category:
			self.set_default_template()
	
	def set_default_template(self):
		"""Set default template based on category"""
		category_templates = {
			"Printing": """
			<h4>Printing Services</h4>
			<table style="width: 100%; border-collapse: collapse;">
				<tr style="background: #f8f9fa;">
					<th style="border: 1px solid #ddd; padding: 8px;">Item</th>
					<th style="border: 1px solid #ddd; padding: 8px;">Quantity</th>
					<th style="border: 1px solid #ddd; padding: 8px;">Specifications</th>
					<th style="border: 1px solid #ddd; padding: 8px;">Unit Price</th>
					<th style="border: 1px solid #ddd; padding: 8px;">Total</th>
				</tr>
				<tr>
					<td style="border: 1px solid #ddd; padding: 8px;">Business Cards</td>
					<td style="border: 1px solid #ddd; padding: 8px;">{{quantity}}</td>
					<td style="border: 1px solid #ddd; padding: 8px;">{{specifications}}</td>
					<td style="border: 1px solid #ddd; padding: 8px;">{{unit_price}}</td>
					<td style="border: 1px solid #ddd; padding: 8px;">{{total_price}}</td>
				</tr>
			</table>
			""",
			"Accounting": """
			<h4>Accounting Services</h4>
			<table style="width: 100%; border-collapse: collapse;">
				<tr style="background: #f8f9fa;">
					<th style="border: 1px solid #ddd; padding: 8px;">Service</th>
					<th style="border: 1px solid #ddd; padding: 8px;">Period</th>
					<th style="border: 1px solid #ddd; padding: 8px;">Scope</th>
					<th style="border: 1px solid #ddd; padding: 8px;">Monthly Fee</th>
				</tr>
				<tr>
					<td style="border: 1px solid #ddd; padding: 8px;">{{service_type}}</td>
					<td style="border: 1px solid #ddd; padding: 8px;">{{period}}</td>
					<td style="border: 1px solid #ddd; padding: 8px;">{{scope}}</td>
					<td style="border: 1px solid #ddd; padding: 8px;">{{monthly_fee}}</td>
				</tr>
			</table>
			""",
			"Digital Marketing": """
			<h4>Digital Marketing Services</h4>
			<table style="width: 100%; border-collapse: collapse;">
				<tr style="background: #f8f9fa;">
					<th style="border: 1px solid #ddd; padding: 8px;">Service</th>
					<th style="border: 1px solid #ddd; padding: 8px;">Duration</th>
					<th style="border: 1px solid #ddd; padding: 8px;">Deliverables</th>
					<th style="border: 1px solid #ddd; padding: 8px;">Cost</th>
				</tr>
				<tr>
					<td style="border: 1px solid #ddd; padding: 8px;">{{service_type}}</td>
					<td style="border: 1px solid #ddd; padding: 8px;">{{duration}}</td>
					<td style="border: 1px solid #ddd; padding: 8px;">{{deliverables}}</td>
					<td style="border: 1px solid #ddd; padding: 8px;">{{cost}}</td>
				</tr>
			</table>
			"""
		}
		
		self.template_content = category_templates.get(self.category, """
		<h4>Service Details</h4>
		<p>Service will be provided as per customer requirements.</p>
		<p><strong>Estimated Cost:</strong> {{estimated_cost}}</p>
		""")
	
	def get_processed_template(self, variables_data=None):
		"""Process template with provided variables"""
		if not self.template_content:
			return ""
		
		template = self.template_content
		
		# Get template variables
		template_vars = {}
		if self.variables:
			try:
				template_vars = json.loads(self.variables)
			except json.JSONDecodeError:
				pass
		
		# Merge with provided variables
		if variables_data:
			template_vars.update(variables_data)
		
		# Replace template variables
		for key, value in template_vars.items():
			template = template.replace(f"{{{{{key}}}}}", str(value))
		
		return template
	
	@staticmethod
	def get_template_for_category(category):
		"""Get BOQ template for a service category"""
		template = frappe.get_value("BOQ Template", 
			{"category": category}, 
			["template_content", "variables"], as_dict=True)
		
		if template:
			return template
		
		# Return None if no template found
		return None
	
	def duplicate_template(self, new_name):
		"""Create a duplicate of this template"""
		new_template = frappe.copy_doc(self)
		new_template.template_name = new_name
		new_template.insert()
		return new_template 
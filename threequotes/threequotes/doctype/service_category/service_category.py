# Copyright (c) 2025, ananthuuuu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ServiceCategory(Document):
	def validate(self):
		"""Validate the service category before saving"""
		self.validate_category_name()
		self.set_default_prompt_template()
	
	def validate_category_name(self):
		"""Ensure category name is unique and properly formatted"""
		if self.category_name:
			# Convert to title case for consistency
			self.category_name = self.category_name.title()
	
	def set_default_prompt_template(self):
		"""Set default AI prompt template if not provided"""
		if not self.ai_prompt_template:
			if self.category_name:
				category_lower = self.category_name.lower()
				if "print" in category_lower:
					self.ai_prompt_template = "What type of printing do you need? How many copies? What size and format?"
				elif "account" in category_lower:
					self.ai_prompt_template = "What accounting services do you need? Monthly/yearly? Number of transactions?"
				elif "marketing" in category_lower or "digital" in category_lower:
					self.ai_prompt_template = "What marketing services do you need? Social media? SEO? PPC advertising?"
				else:
					self.ai_prompt_template = f"What {self.category_name.lower()} services do you need? Please provide details about your requirements."
	
	def before_save(self):
		"""Set default values before saving"""
		if not self.status:
			self.status = "Active"
		
		# Set default icon if not provided
		if not self.icon:
			category_lower = self.category_name.lower() if self.category_name else ""
			if "print" in category_lower:
				self.icon = "fa fa-print"
			elif "account" in category_lower:
				self.icon = "fa fa-calculator"
			elif "marketing" in category_lower or "digital" in category_lower:
				self.icon = "fa fa-bullhorn"
			else:
				self.icon = "fa fa-briefcase"
	
	def get_active_vendors(self):
		"""Get all active vendors for this service category"""
		return frappe.get_all("Vendor", 
			filters={
				"status": "Active"
			},
			fields=["name", "vendor_name", "email", "phone", "rating"]
		)
	
	@staticmethod
	def get_active_categories():
		"""Get all active service categories"""
		return frappe.get_all("Service Category", 
			filters={"status": "Active"},
			fields=["name", "category_name", "description", "icon"],
			order_by="category_name"
		)

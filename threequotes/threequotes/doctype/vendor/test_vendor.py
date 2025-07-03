# Copyright (c) 2025, ananthuuuu and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestVendor(FrappeTestCase):
	def test_vendor_creation(self):
		"""Test basic vendor creation"""
		vendor = frappe.get_doc({
			"doctype": "Vendor",
			"vendor_name": "Test Vendor",
			"email": "test@vendor.com",
			"phone": "1234567890",
			"status": "Active",
			"service_categories": [{
				"service_category": "Printing"
			}]
		})
		vendor.insert()
		
		self.assertEqual(vendor.vendor_name, "Test Vendor")
		self.assertEqual(vendor.status, "Active")
		self.assertEqual(len(vendor.service_categories), 1)
		
		# Clean up
		vendor.delete()
	
	def test_email_validation(self):
		"""Test email validation"""
		vendor = frappe.get_doc({
			"doctype": "Vendor",
			"vendor_name": "Test Vendor",
			"email": "invalid-email",
			"service_categories": [{
				"service_category": "Printing"
			}]
		})
		
		with self.assertRaises(frappe.ValidationError):
			vendor.insert()
	
	def test_service_category_validation(self):
		"""Test service category validation"""
		vendor = frappe.get_doc({
			"doctype": "Vendor",
			"vendor_name": "Test Vendor",
			"email": "test@vendor.com",
			"service_categories": []  # No service categories
		})
		
		with self.assertRaises(frappe.ValidationError):
			vendor.insert() 
# Copyright (c) 2025, ananthuuuu and contributors
# For license information, please see license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestServiceRequest(FrappeTestCase):
	def test_service_request_creation(self):
		"""Test basic service request creation"""
		service_request = frappe.get_doc({
			"doctype": "Service Request",
			"customer_name": "Test Customer",
			"customer_email": "test@customer.com",
			"service_category": "Printing",
			"chat_transcript": "I need business cards printed"
		})
		service_request.insert()
		
		self.assertEqual(service_request.customer_name, "Test Customer")
		self.assertEqual(service_request.status, "Draft")
		
		# Clean up
		service_request.delete()
	
	def test_boq_generation(self):
		"""Test BOQ generation"""
		service_request = frappe.get_doc({
			"doctype": "Service Request",
			"customer_name": "Test Customer",
			"customer_email": "test@customer.com",
			"service_category": "Printing",
			"chat_transcript": "I need 1000 business cards"
		})
		service_request.insert()
		
		# BOQ should be generated automatically
		self.assertTrue(service_request.boq_generated)
		self.assertEqual(service_request.status, "BOQ Generated")
		
		# Clean up
		service_request.delete()
	
	def test_email_validation(self):
		"""Test email validation"""
		service_request = frappe.get_doc({
			"doctype": "Service Request",
			"customer_name": "Test Customer",
			"customer_email": "invalid-email",
			"service_category": "Printing"
		})
		
		with self.assertRaises(frappe.ValidationError):
			service_request.insert() 
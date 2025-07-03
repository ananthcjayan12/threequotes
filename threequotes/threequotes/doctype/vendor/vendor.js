// Copyright (c) 2025, ananthuuuu and contributors
// For license information, please see license.txt

frappe.ui.form.on("Vendor", {
	refresh(frm) {
		// Add custom buttons for vendor actions
		if (frm.doc.name) {
			frm.add_custom_button(__('View Service Requests'), function() {
				frappe.route_options = {
					"vendor": frm.doc.name
				};
				frappe.set_route("List", "Quote Response");
			});
			
			frm.add_custom_button(__('Send Test Email'), function() {
				frappe.call({
					method: 'frappe.core.doctype.communication.email.make',
					args: {
						recipients: frm.doc.email,
						subject: 'Test Email from 3kwotes',
						content: 'This is a test email to verify your email address.',
						send_email: 1
					},
					callback: function(r) {
						if (r.message) {
							frappe.msgprint(__('Test email sent successfully'));
						}
					}
				});
			});
		}
		
		// Set indicator based on status
		frm.set_indicator_formatter('status', function(doc) {
			return doc.status === 'Active' ? 'green' : 'red';
		});
	},
	
	email(frm) {
		// Validate email format on change
		if (frm.doc.email) {
			if (!frappe.utils.validate_type(frm.doc.email, 'email')) {
				frappe.msgprint(__('Please enter a valid email address'));
				frm.set_value('email', '');
			}
		}
	},
	
	rating(frm) {
		// Show rating description
		if (frm.doc.rating) {
			let descriptions = {
				1: 'Poor',
				2: 'Fair', 
				3: 'Good',
				4: 'Very Good',
				5: 'Excellent'
			};
			frm.set_df_property('rating', 'description', descriptions[frm.doc.rating] || '');
		}
	},
	
	status(frm) {
		// Show warning if deactivating vendor with pending quotes
		if (frm.doc.status === 'Inactive' && frm.doc.name) {
			frappe.call({
				method: 'frappe.client.get_count',
				args: {
					doctype: 'Quote Response',
					filters: {
						vendor: frm.doc.name,
						status: 'Pending'
					}
				},
				callback: function(r) {
					if (r.message > 0) {
						frappe.msgprint({
							title: __('Warning'),
							message: __('This vendor has {0} pending quote responses. Deactivating may affect ongoing processes.', [r.message]),
							indicator: 'orange'
						});
					}
				}
			});
		}
	}
});

// Child table: Service Categories
frappe.ui.form.on("Vendor Service Category", {
	service_category(frm, cdt, cdn) {
		// Auto-refresh form when service category is selected
		let row = locals[cdt][cdn];
		if (row.service_category) {
			// You can add any validation or auto-fill logic here
			frm.refresh_field('service_categories');
		}
	}
});

// List view customization
frappe.listview_settings['Vendor'] = {
	add_fields: ['status', 'rating', 'response_time'],
	get_indicator: function(doc) {
		if (doc.status === 'Active') {
			return [__('Active'), 'green', 'status,=,Active'];
		} else {
			return [__('Inactive'), 'red', 'status,=,Inactive'];
		}
	},
	formatters: {
		vendor_name: function(value, field, doc) {
			let rating_stars = '';
			if (doc.rating) {
				rating_stars = ' ' + '★'.repeat(doc.rating) + '☆'.repeat(5 - doc.rating);
			}
			return value + rating_stars;
		},
		response_time: function(value, field, doc) {
			if (value) {
				return value + ' hrs';
			}
			return value;
		}
	}
}; 
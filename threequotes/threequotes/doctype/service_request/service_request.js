// Copyright (c) 2025, ananthuuuu and contributors
// For license information, please see license.txt

frappe.ui.form.on("Service Request", {
	refresh(frm) {
		// Set status indicator
		frm.set_indicator_formatter('status', function(doc) {
			const status_colors = {
				'Draft': 'grey',
				'BOQ Generated': 'blue',
				'Sent to Vendors': 'orange',
				'Quotes Received': 'green',
				'Completed': 'green',
				'Cancelled': 'red'
			};
			return status_colors[doc.status] || 'grey';
		});
		
		// Add custom buttons based on status
		if (frm.doc.name) {
			// Generate BOQ button
			if (frm.doc.status === 'Draft' && frm.doc.chat_transcript) {
				frm.add_custom_button(__('Generate BOQ'), function() {
					frm.call('generate_boq').then(() => {
						frm.refresh();
					});
				});
			}
			
			// View Quotes button
			if (frm.doc.status === 'Quotes Received' || frm.doc.status === 'Completed') {
				frm.add_custom_button(__('View Quotes'), function() {
					frappe.route_options = {
						"service_request": frm.doc.name
					};
					frappe.set_route("List", "Quote Response");
				});
			}
			
			// Send to Vendors button (for testing)
			if (frm.doc.status === 'BOQ Generated' && frm.doc.docstatus === 0) {
				frm.add_custom_button(__('Send to Vendors'), function() {
					frappe.confirm(
						__('Are you sure you want to send this BOQ to vendors?'),
						function() {
							frappe.call({
				method: 'threequotes.threequotes.doctype.service_request.service_request.send_boq_to_vendors',
				args: {
					request_id: frm.doc.name
				}
			}).then(() => {
								frm.refresh();
							});
						}
					);
				});
			}
		}
		
		// Show BOQ preview if available
		if (frm.doc.boq_generated) {
			frm.add_custom_button(__('Preview BOQ'), function() {
				let d = new frappe.ui.Dialog({
					title: __('BOQ Preview'),
					fields: [
						{
							fieldname: 'boq_preview',
							fieldtype: 'HTML',
							options: frm.doc.boq_generated
						}
					],
					size: 'large'
				});
				d.show();
			});
		}
	},
	
	service_category(frm) {
		// Auto-generate BOQ when service category is selected
		if (frm.doc.service_category && frm.doc.chat_transcript && !frm.doc.boq_generated) {
			frm.call('generate_boq').then(() => {
				frm.refresh();
			});
		}
		
		// Show AI prompt template for the selected category
		if (frm.doc.service_category) {
			frappe.call({
				method: 'frappe.client.get_value',
				args: {
					doctype: 'Service Category',
					filters: {name: frm.doc.service_category},
					fieldname: 'ai_prompt_template'
				},
				callback: function(r) {
					if (r.message && r.message.ai_prompt_template) {
						frm.set_df_property('chat_transcript', 'description', 
							'Suggested questions: ' + r.message.ai_prompt_template);
					}
				}
			});
		}
	},
	
	chat_transcript(frm) {
		// Auto-generate BOQ when chat transcript is updated
		if (frm.doc.chat_transcript && frm.doc.service_category && !frm.doc.boq_generated) {
			// Debounced BOQ generation
			clearTimeout(frm.boq_timeout);
			frm.boq_timeout = setTimeout(() => {
				frm.call('generate_boq').then(() => {
					frm.refresh();
				});
			}, 2000);
		}
	},
	
	customer_email(frm) {
		// Validate email format
		if (frm.doc.customer_email) {
			if (!frappe.utils.validate_type(frm.doc.customer_email, 'email')) {
				frappe.msgprint(__('Please enter a valid email address'));
				frm.set_value('customer_email', '');
			}
		}
	},
	
	before_submit(frm) {
		// Validate before submission
		if (!frm.doc.boq_generated) {
			frappe.msgprint(__('Please generate BOQ before submitting'));
			frappe.validated = false;
			return;
		}
		
		// Confirm submission
		frappe.confirm(
			__('This will send the BOQ to vendors. Are you sure you want to proceed?'),
			function() {
				// Proceed with submission
			},
			function() {
				frappe.validated = false;
			}
		);
	}
});

// List view customization
frappe.listview_settings['Service Request'] = {
	add_fields: ['status', 'service_category', 'created_date'],
	get_indicator: function(doc) {
		const status_colors = {
			'Draft': ['Draft', 'grey'],
			'BOQ Generated': ['BOQ Generated', 'blue'],
			'Sent to Vendors': ['Sent to Vendors', 'orange'],
			'Quotes Received': ['Quotes Received', 'green'],
			'Completed': ['Completed', 'green'],
			'Cancelled': ['Cancelled', 'red']
		};
		return status_colors[doc.status] || ['Unknown', 'grey'];
	},
	formatters: {
		customer_name: function(value, field, doc) {
			return `${value} <small style="color: #888;">(${doc.service_category})</small>`;
		}
	}
}; 
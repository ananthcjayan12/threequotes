// Copyright (c) 2025, ananthuuuu and contributors
// For license information, please see license.txt

frappe.ui.form.on("Service Category", {
	refresh(frm) {
		// Add custom buttons for quick actions
		if (frm.doc.name) {
			frm.add_custom_button(__('View Service Requests'), function() {
				frappe.route_options = {
					"service_category": frm.doc.name
				};
				frappe.set_route("List", "Service Request");
			});
			
			frm.add_custom_button(__('Create BOQ Template'), function() {
				frappe.new_doc("BOQ Template", {
					category: frm.doc.name
				});
			});
		}
		
		// Set icon preview if icon field has value
		if (frm.doc.icon) {
			frm.set_df_property('icon', 'description', 
				`<i class="${frm.doc.icon}"></i> Preview: ${frm.doc.icon}`
			);
		}
	},
	
	category_name(frm) {
		// Auto-generate slug/name from category name
		if (frm.doc.category_name && !frm.doc.name) {
			frm.doc.name = frm.doc.category_name.toLowerCase().replace(/\s+/g, '-');
		}
	},
	
	icon(frm) {
		// Show icon preview when icon field changes
		if (frm.doc.icon) {
			frm.set_df_property('icon', 'description', 
				`<i class="${frm.doc.icon}"></i> Preview: ${frm.doc.icon}`
			);
		} else {
			frm.set_df_property('icon', 'description', 
				'CSS class for icon (e.g., fa fa-print)'
			);
		}
	},
	
	status(frm) {
		// Show warning if deactivating a category that has active service requests
		if (frm.doc.status === 'Inactive' && frm.doc.name) {
			frappe.call({
				method: 'frappe.client.get_count',
				args: {
					doctype: 'Service Request',
					filters: {
						service_category: frm.doc.name,
						status: ['!=', 'Completed']
					}
				},
				callback: function(r) {
					if (r.message > 0) {
						frappe.msgprint({
							title: __('Warning'),
							message: __('This category has {0} active service requests. Deactivating it may affect ongoing processes.', [r.message]),
							indicator: 'orange'
						});
					}
				}
			});
		}
	}
});

// List view customization
frappe.listview_settings['Service Category'] = {
	add_fields: ['status', 'icon'],
	get_indicator: function(doc) {
		if (doc.status === 'Active') {
			return [__('Active'), 'green', 'status,=,Active'];
		} else {
			return [__('Inactive'), 'red', 'status,=,Inactive'];
		}
	},
	formatters: {
		category_name: function(value, field, doc) {
			let icon = doc.icon ? `<i class="${doc.icon}"></i> ` : '';
			return `${icon}${value}`;
		}
	}
};

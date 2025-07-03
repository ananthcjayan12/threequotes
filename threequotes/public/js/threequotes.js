/* 3kwotes - Main JavaScript File */

// Common utilities and functions
window.ThreeQuotes = {
    // Initialize the application
    init: function() {
        this.setupCommonElements();
        this.setupFormValidation();
        this.setupLoadingStates();
    },

    // Setup common UI elements
    setupCommonElements: function() {
        // Add smooth scrolling to anchor links
        $('a[href^="#"]').on('click', function(event) {
            var target = $(this.getAttribute('href'));
            if(target.length) {
                event.preventDefault();
                $('html, body').stop().animate({
                    scrollTop: target.offset().top - 80
                }, 1000);
            }
        });

        // Auto-hide alerts after 5 seconds
        setTimeout(function() {
            $('.alert').fadeOut();
        }, 5000);

        // Initialize tooltips
        if (typeof bootstrap !== 'undefined') {
            var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
        }
    },

    // Setup form validation
    setupFormValidation: function() {
        // Email validation
        $('input[type="email"]').on('blur', function() {
            const email = $(this).val();
            if (email && !ThreeQuotes.isValidEmail(email)) {
                $(this).addClass('is-invalid');
                $(this).siblings('.invalid-feedback').text('Please enter a valid email address');
            } else {
                $(this).removeClass('is-invalid');
            }
        });

        // Phone validation
        $('input[type="tel"]').on('input', function() {
            let value = $(this).val().replace(/[^\d+\-\s\(\)]/g, '');
            $(this).val(value);
        });

        // Required field validation
        $('input[required], textarea[required], select[required]').on('blur', function() {
            if (!$(this).val().trim()) {
                $(this).addClass('is-invalid');
            } else {
                $(this).removeClass('is-invalid');
            }
        });
    },

    // Setup loading states for buttons
    setupLoadingStates: function() {
        $(document).on('click', '.btn[data-loading-text]', function() {
            const btn = $(this);
            const loadingText = btn.data('loading-text');
            const originalText = btn.html();
            
            btn.data('original-text', originalText);
            btn.html('<i class="fa fa-spinner fa-spin"></i> ' + loadingText);
            btn.prop('disabled', true);
        });
    },

    // Utility functions
    isValidEmail: function(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    },

    isValidPhone: function(phone) {
        const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
        return phoneRegex.test(phone.replace(/[\s\-\(\)]/g, ''));
    },

    formatCurrency: function(amount) {
        return '₹' + Number(amount).toLocaleString('en-IN');
    },

    formatDate: function(date) {
        return new Date(date).toLocaleDateString('en-IN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    },

    // Show notification messages
    showNotification: function(message, type = 'info') {
        const alertClass = `alert-${type}`;
        const alertHtml = `
            <div class="alert ${alertClass} alert-dismissible fade show position-fixed" 
                 style="top: 20px; right: 20px; z-index: 9999; min-width: 300px;" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        $('body').append(alertHtml);
        
        // Auto remove after 5 seconds
        setTimeout(function() {
            $('.alert').fadeOut();
        }, 5000);
    },

    // API call wrapper
    apiCall: function(method, args, callback, errorCallback) {
        frappe.call({
            method: method,
            args: args,
            callback: function(response) {
                if (response.message) {
                    if (callback) callback(response.message);
                } else {
                    if (errorCallback) errorCallback('No response received');
                }
            },
            error: function(xhr, status, error) {
                if (errorCallback) errorCallback(error);
            }
        });
    },

    // Form submission helper
    submitForm: function(formId, endpoint, successCallback, errorCallback) {
        const form = $(formId);
        const formData = new FormData(form[0]);
        
        // Show loading state
        const submitBtn = form.find('button[type="submit"]');
        const originalText = submitBtn.html();
        submitBtn.prop('disabled', true).html('<i class="fa fa-spinner fa-spin"></i> Submitting...');
        
        // Convert FormData to object
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });
        
        this.apiCall(endpoint, data, 
            function(response) {
                submitBtn.prop('disabled', false).html(originalText);
                if (successCallback) successCallback(response);
            },
            function(error) {
                submitBtn.prop('disabled', false).html(originalText);
                if (errorCallback) errorCallback(error);
            }
        );
    },

    // File upload helper
    uploadFile: function(fileInput, callback) {
        const file = fileInput.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);
        formData.append('is_private', 0);

        $.ajax({
            url: '/api/method/upload_file',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (callback) callback(response.message);
            },
            error: function() {
                ThreeQuotes.showNotification('File upload failed', 'danger');
            }
        });
    }
};

// Service Request specific functions
window.ServiceRequest = {
    create: function(data, callback) {
        ThreeQuotes.apiCall('frappe.client.insert', {
            doc: Object.assign({doctype: 'Service Request'}, data)
        }, callback);
    },

    generateBOQ: function(requestId, callback) {
        ThreeQuotes.apiCall(
            'threequotes.threequotes.doctype.service_request.service_request.generate_boq',
            {request_id: requestId},
            callback
        );
    },

    sendToVendors: function(requestId, callback) {
        ThreeQuotes.apiCall(
            'threequotes.threequotes.doctype.service_request.service_request.send_boq_to_vendors',
            {request_id: requestId},
            callback
        );
    }
};

// Quote Response specific functions
window.QuoteResponse = {
    create: function(data, callback) {
        ThreeQuotes.apiCall('frappe.client.insert', {
            doc: Object.assign({doctype: 'Quote Response'}, data)
        }, callback);
    },

    getByRequest: function(requestId, callback) {
        ThreeQuotes.apiCall('frappe.client.get_list', {
            doctype: 'Quote Response',
            filters: {service_request: requestId},
            fields: ['*']
        }, callback);
    }
};

// Vendor specific functions
window.Vendor = {
    sendTestEmail: function(vendorId, callback) {
        ThreeQuotes.apiCall(
            'threequotes.threequotes.doctype.vendor.vendor.send_test_email',
            {vendor_id: vendorId},
            callback
        );
    },

    getByCategory: function(categoryId, callback) {
        ThreeQuotes.apiCall('frappe.client.get_list', {
            doctype: 'Vendor Service Category',
            filters: {service_category: categoryId},
            fields: ['parent']
        }, function(response) {
            const vendorIds = response.map(r => r.parent);
            if (vendorIds.length > 0) {
                ThreeQuotes.apiCall('frappe.client.get_list', {
                    doctype: 'Vendor',
                    filters: [['name', 'in', vendorIds]],
                    fields: ['*']
                }, callback);
            } else {
                callback([]);
            }
        });
    }
};

// Initialize when document is ready
$(document).ready(function() {
    ThreeQuotes.init();
    
    // Add any page-specific initialization
    if (window.location.pathname === '/request') {
        // Request page specific code
        console.log('Request page loaded');
    } else if (window.location.pathname === '/vendor') {
        // Vendor page specific code
        console.log('Vendor page loaded');
    } else if (window.location.pathname === '/admin') {
        // Admin page specific code
        console.log('Admin page loaded');
    }
});

// Expose functions globally for inline onclick handlers
window.generateBOQ = function(requestId) {
    if (confirm('Generate BOQ for this request?')) {
        ServiceRequest.generateBOQ(requestId, function(response) {
            ThreeQuotes.showNotification('BOQ generated successfully!', 'success');
            setTimeout(() => location.reload(), 1000);
        });
    }
};

window.sendToVendors = function(requestId) {
    if (confirm('Send this BOQ to all relevant vendors?')) {
        ServiceRequest.sendToVendors(requestId, function(response) {
            ThreeQuotes.showNotification('BOQ sent to vendors successfully!', 'success');
            setTimeout(() => location.reload(), 1000);
        });
    }
};

window.viewQuotes = function(requestId) {
    window.open('/app/quote-response?service_request=' + requestId, '_blank');
};

window.testVendorEmail = function(vendorId) {
    Vendor.sendTestEmail(vendorId, function(response) {
        ThreeQuotes.showNotification('Test email sent successfully!', 'success');
    });
}; 
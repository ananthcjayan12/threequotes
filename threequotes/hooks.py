app_name = "threequotes"
app_title = "Threequotes"
app_publisher = "ananthuuuu"
app_description = "Quotation management software"
app_email = "ananthcjayan12@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "threequotes",
# 		"logo": "/assets/threequotes/logo.png",
# 		"title": "Threequotes",
# 		"route": "/threequotes",
# 		"has_permission": "threequotes.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/threequotes/css/threequotes.css"
# app_include_js = "/assets/threequotes/js/threequotes.js"

# include js, css files in header of web template
# web_include_css = "/assets/threequotes/css/threequotes.css"
# web_include_js = "/assets/threequotes/js/threequotes.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "threequotes/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "threequotes/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "threequotes.utils.jinja_methods",
# 	"filters": "threequotes.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "threequotes.install.before_install"
# after_install = "threequotes.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "threequotes.uninstall.before_uninstall"
# after_uninstall = "threequotes.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "threequotes.utils.before_app_install"
# after_app_install = "threequotes.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "threequotes.utils.before_app_uninstall"
# after_app_uninstall = "threequotes.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "threequotes.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"threequotes.tasks.all"
# 	],
# 	"daily": [
# 		"threequotes.tasks.daily"
# 	],
# 	"hourly": [
# 		"threequotes.tasks.hourly"
# 	],
# 	"weekly": [
# 		"threequotes.tasks.weekly"
# 	],
# 	"monthly": [
# 		"threequotes.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "threequotes.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "threequotes.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "threequotes.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["threequotes.utils.before_request"]
# after_request = ["threequotes.utils.after_request"]

# Job Events
# ----------
# before_job = ["threequotes.utils.before_job"]
# after_job = ["threequotes.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"threequotes.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Web pages - these will be accessible as URLs
website_route_rules = [
	{"from_route": "/admin", "to_route": "admin"},
	{"from_route": "/vendor", "to_route": "vendor"},
	{"from_route": "/request", "to_route": "request"},
]

# Include CSS and JS files for web pages
web_include_css = [
	"assets/threequotes/css/threequotes.css"
]

web_include_js = [
	"assets/threequotes/js/threequotes.js"
]

# Website settings
website_generators = []

# Email settings
email_brand_image = ""
default_mail_footer = """
<div style="text-align: center; margin-top: 20px; padding: 20px; border-top: 1px solid #eee;">
	<p style="margin: 0; color: #666; font-size: 12px;">
		This email was sent by 3kwotes - Get quotes from verified vendors
	</p>
</div>
"""


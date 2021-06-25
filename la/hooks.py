from . import __version__ as app_version

app_name = "la"
app_title = "La"
app_publisher = "GreyCube Technologies"
app_description = "Customization for LA"
app_icon = "octicon octicon-file-directory"
app_color = "green"
app_email = "admin@greycube.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/la/css/la.css"
# app_include_js = "/assets/la/js/la.js"

# include js, css files in header of web template
# web_include_css = "/assets/la/css/la.css"
# web_include_js = "/assets/la/js/la.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "la/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Material Request" : "public/js/material_request.js",
	"Sales Invoice" : "public/js/sales_invoice.js"
	}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "la.install.before_install"
# after_install = "la.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "la.notifications.get_notification_config"

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

doc_events = {
	"Stock Entry": {
		"on_submit": "la.api.check_approvals_and_update_mr_status_based_on_completed_qty",
		"validate": "la.api.check_approvals_on_save_for_stock_entry",
		"on_cancel":"la.api.update_material_request_status_cf_based_on_completed_qty"
	},
	"Sales Invoice":{
		"validate":"la.api.sales_invoice_update_payment_information_for_pos_and_restrict_warehouse"
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"la.tasks.all"
# 	],
# 	"daily": [
# 		"la.tasks.daily"
# 	],
# 	"hourly": [
# 		"la.tasks.hourly"
# 	],
# 	"weekly": [
# 		"la.tasks.weekly"
# 	]
# 	"monthly": [
# 		"la.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "la.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "la.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "la.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"la.auth.validate"
# ]


# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "project_invoice"
app_title = "Project Invoice"
app_publisher = "Hardik Gadesha"
app_description = "Invoice"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "hardikgadesha@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/project_invoice/css/project_invoice.css"
# app_include_js = "/assets/project_invoice/js/project_invoice.js"

# include js, css files in header of web template
# web_include_css = "/assets/project_invoice/css/project_invoice.css"
# web_include_js = "/assets/project_invoice/js/project_invoice.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "project_invoice/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views

doctype_js = {
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

# before_install = "project_invoice.install.before_install"
# after_install = "project_invoice.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "project_invoice.notifications.get_notification_config"

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
	"Project": {
		"validate": "project_invoice.project_invoice.invoice.createItem",
		"on_update": "project_invoice.project_invoice.invoice.UpdatePrice"
	},
	"Delivery Note": {
                "on_submit": "project_invoice.project_invoice.invoice.updateMaterialCost",
		"on_cancel": "project_invoice.project_invoice.invoice.revertMaterialCost"
        },
	"Sales Invoice": {
                "on_submit": "project_invoice.project_invoice.invoice.UpdateProjectStatus",
                "on_cancel": "project_invoice.project_invoice.invoice.RevertProjectStatus"
        },
	"Task": {
		"after_insert": "project_invoice.project_invoice.invoice.UpdateTaskCost",
                "on_update": "project_invoice.project_invoice.invoice.UpdateTaskCost"
        },
	"Timesheet": {
                "on_submit": "project_invoice.project_invoice.invoice.UpdateLabourCost"
        }
}

fixtures = [
    {
	"doctype": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                [
			"Sales Invoice-invoice_type",
			"Project-washing_and_material_costing",
			"Project-washing_cost",
			"Project-column_break_42",
			"Project-material_cost",
			"Sales Invoice-project_details",
			"Sales Invoice-project_table",
			"Sales Invoice Item-section_break_33",
			"Sales Invoice Item-labour",
			"Sales Invoice Item-materiel",
			"Sales Invoice Item-washing",
			"Sales Invoice Item-count_rate",
			"Item-is_project",
			"Sales Invoice-total_labour",
			"Sales Invoice-total_washing",
			"Sales Invoice-total_material",
			"Task-total_task_cost",
			"Project-column_break_44",
			"Project-labour_cost"
                ]
            ]
        ]
 },
 {
	"doctype": "Property Setter",
        "filters": [
            [
                "name",
                "in",
                [
			"Sales Invoice-items_section-depends_on",
			"Project-total_billable_amount-default"
                ]
            ]
        ]
 }
]

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"project_invoice.tasks.all"
# 	],
# 	"daily": [
# 		"project_invoice.tasks.daily"
# 	],
# 	"hourly": [
# 		"project_invoice.tasks.hourly"
# 	],
# 	"weekly": [
# 		"project_invoice.tasks.weekly"
# 	]
# 	"monthly": [
# 		"project_invoice.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "project_invoice.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "project_invoice.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "project_invoice.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


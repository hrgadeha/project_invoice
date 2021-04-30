from __future__ import unicode_literals
import frappe
from frappe.utils import cint, cstr, formatdate, flt, getdate, nowdate, get_link_to_form
from datetime import date
from frappe import msgprint
from frappe.model.document import Document

@frappe.whitelist(allow_guest=True)
def createItem(doc,method):
	if not frappe.db.exists('Price List', "Project Price List"):
		pricelist = frappe.get_doc({
		"doctype": "Price List",
		"price_list_name": "Project Price List",
		"selling": 1
		})
		pricelist.insert(ignore_permissions=True,ignore_mandatory = True)
		pricelist.save()

	if not frappe.db.exists('Item Group', "Project"):
		item_group = frappe.get_doc({
		"doctype": "Item Group",
		"item_group_name": "Project",
		"parent_item_group": "All Item Groups"
		})
		item_group.insert(ignore_permissions=True,ignore_mandatory = True)
		item_group.save()

	if not frappe.db.exists('Item', doc.name):
		item = frappe.get_doc({
		"doctype": "Item",
		"item_code": doc.name,
		"item_name": doc.name,
		"description": doc.project_name,
		"is_project": 1,
		"is_stock_item": 0,
		"include_item_in_manufacturing": 0,
		"stock_uom": "Nos",
		"item_group": "Project",
		"is_purchase_item": 0
		})
		item.insert(ignore_permissions=True,ignore_mandatory = True)
		item.save(ignore_permissions=True)

@frappe.whitelist(allow_guest=True)
def UpdatePrice(doc,method):
	price = flt(doc.total_billable_amount) + flt(doc.washing_cost) + flt(doc.material_cost)
	item_price = frappe.db.sql("""select name from `tabItem Price` where item_code = %s and price_list = "Project Price List"
			;""",(doc.name))
	if item_price:
		ip = frappe.get_doc("Item Price",item_price[0][0])
		ip.price_list_rate = price
		ip.save()

	if not item_price:
		item_pr = frappe.get_doc(dict(
		doctype = "Item Price",
		item_code = doc.name,
		selling = 1,
		price_list = "Project Price List",
		price_list_rate = price,
		valid_from = date.today()
		)).insert(ignore_permissions = True,ignore_mandatory = True)
		item_pr.save()

@frappe.whitelist(allow_guest=True)
def getLabour(project):
	labour = frappe.db.sql("""select name,total_billable_hours,total_billable_amount from `tabTimesheet` where parent_project = %s and 
		docstatus = 1 and status != "Billed";""",(project),as_list = True)
	return labour if labour else 0


@frappe.whitelist(allow_guest=True)
def updateMaterialCost(doc,method):
	if doc.project:
		project = frappe.get_doc("Project",doc.project)
		project.material_cost += doc.total
		project.save(ignore_permissions=True)


@frappe.whitelist(allow_guest=True)
def revertMaterialCost(doc,method):
	if doc.project:
		project = frappe.get_doc("Project",doc.project)
		project.material_cost -= doc.total
		project.save(ignore_permissions=True)

@frappe.whitelist(allow_guest=True)
def UpdateProjectStatus(doc,method):
	if doc.invoice_type == "Project Invoice":
		for d in doc.project_table:
			pro = frappe.get_doc("Project",d.project_code)
			pro.percent_complete_method = "Manual"
			pro.percent_complete = 100
			pro.status = "Completed"
			pro.save(ignore_permissions=True)


@frappe.whitelist(allow_guest=True)
def RevertProjectStatus(doc,method):
	if doc.invoice_type == "Project Invoice":
		for d in doc.project_table:
			pro = frappe.get_doc("Project",d.project_code)
			pro.percent_complete = 0
			pro.percent_complete_method = "Manual"
			pro.status = "Open"
			pro.save(ignore_permissions=True)


@frappe.whitelist(allow_guest=True)
def UpdateTaskCost(doc,method):
	total_washing = 0
	for d in frappe.get_list('Task',filters={'project': doc.project},fields=('total_task_cost')):
		total_washing += d.total_task_cost
	pro = frappe.get_doc("Project",doc.project)
	pro.washing_cost = total_washing
	pro.save()

@frappe.whitelist(allow_guest=True)
def UpdateLabourCost(doc,method):
        total_labour = 0
        for d in frappe.get_list('Timesheet',filters={'parent_project': doc.parent_project},fields=('total_billable_amount')):
                total_labour += d.total_billable_amount
        pro = frappe.get_doc("Project",doc.parent_project)
        pro.labour_cost = total_labour
        pro.save()

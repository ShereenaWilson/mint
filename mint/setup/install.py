import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def after_install():
		custom_fields = {
					"Bank Account": [
									{
														"fieldname": "is_credit_card",
														"fieldtype": "Check",
														"label": "Is Credit Card",
														"insert_after": "bank_account_no",
														"default": 0,
									}
					],
					"Bank Transaction": [
									{
														"fieldname": "is_rule_evaluated",
														"fieldtype": "Check",
														"label": "Is Rule Evaluated",
														"default": 0,
														"allow_on_submit": 1,
														"insert_after": "party",
									},
									{
														"fieldname": "matched_rule",
														"insert_after": "is_rule_evaluated",
														"fieldtype": "Link",
														"label": "Matched Rule",
														"options": "Mint Bank Transaction Rule",
														"read_only": 1,
														"allow_on_submit": 1,
									},
					],
		}

	# Only add reconciliation_type if it is not already a standard field in the DocType
		existing_fieldnames = [
			f.fieldname for f in frappe.get_meta("Bank Transaction Payments").fields
		]
		if "reconciliation_type" not in existing_fieldnames:
					custom_fields["Bank Transaction Payments"] = [
									{
														"fieldname": "reconciliation_type",
														"fieldtype": "Select",
														"label": "Reconciliation Type",
														"options": "Matched\nVoucher Created",
														"insert_after": "clearance_date",
														"read_only": 1,
														"default": "Matched",
									}
					]

		create_custom_fields(custom_fields)

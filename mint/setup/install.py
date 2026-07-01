import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def after_install():
    custom_fields = {}

    bank_account_fieldnames = [
        f.fieldname for f in frappe.get_meta("Bank Account").fields
    ]
    if "is_credit_card" not in bank_account_fieldnames:
        custom_fields["Bank Account"] = [
            {
                "fieldname": "is_credit_card",
                "fieldtype": "Check",
                "label": "Is Credit Card",
                "insert_after": "bank_account_no",
                "default": 0,
            }
        ]

    bank_transaction_fieldnames = [
        f.fieldname for f in frappe.get_meta("Bank Transaction").fields
    ]
    bank_transaction_custom = []
    if "is_rule_evaluated" not in bank_transaction_fieldnames:
        bank_transaction_custom.append(
            {
                "fieldname": "is_rule_evaluated",
                "fieldtype": "Check",
                "label": "Is Rule Evaluated",
                "default": 0,
                "allow_on_submit": 1,
                "insert_after": "party",
            }
        )
    if "matched_rule" not in bank_transaction_fieldnames:
        bank_transaction_custom.append(
            {
                "fieldname": "matched_rule",
                "insert_after": "is_rule_evaluated",
                "fieldtype": "Link",
                "label": "Matched Rule",
                "options": "Mint Bank Transaction Rule",
                "read_only": 1,
                "allow_on_submit": 1,
            }
        )
    if bank_transaction_custom:
        custom_fields["Bank Transaction"] = bank_transaction_custom

    bank_transaction_payments_fieldnames = [
        f.fieldname for f in frappe.get_meta("Bank Transaction Payments").fields
    ]
    if "reconciliation_type" not in bank_transaction_payments_fieldnames:
        custom_fields["Bank Transaction Payments"] = [
            {
                "fieldname": "reconciliation_type",
                "fieldtype": "Select",
                "label": "Reconciliation Type",
                "options": "Matched\nVoucher Created",
                "insert_after": "clearance_date",
            }
        ]

    if custom_fields:
        create_custom_fields(custom_fields)

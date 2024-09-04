# Copyright (c) 2024, dorah and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.model.docstatus import DocStatus
from frappe.utils import today, add_days, add_months


class LibraryMembership(WebsiteGenerator):
    # check before submitting this document
    def validate(self):
        self.check_expiry_date()

    def check_expiry_date(self):
        if self.expiry_date and self.expiry_date < today():
            frappe.throw("Membership expiry date cannot be in the past.")

    def before_insert(self):
        if not self.membership_id:
            self.membership_id = frappe.model.naming.make_autoname('MEM-.#####')

    def extend_membership(self, months):
        self.expiry_date = add_months(self.expiry_date or today(), months)
        self.save()
    def before_submit(self):
        exists = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": DocStatus.submitted(),
                # check if the membership's end date
                "to_date": (">", self.from_date),
            },
        )
        if exists:
            frappe.throw("There is an active membership for this member")
    
    def before_save(self):
        if self.expiry_date and self.expiry_date == add_days(today(), 7):
            self.send_expiry_notification()

    def send_expiry_notification(self):
        if self.member_email:
            frappe.sendmail(
                recipients=[self.member_email],
                subject="Membership Expiry Notification",
                message=f"Dear {self.member_name}, your membership is about to expire on {self.expiry_date}. Please renew it in time."
            )

    def cancel_membership(self):
        self.status = 'Cancelled'
        self.save()

    def validate(self):
        super().validate()
        if self.status == 'Cancelled' and not self.cancellation_reason:
            frappe.throw("Please provide a reason for cancellation.")
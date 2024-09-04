# Copyright (c) 2024, dorah and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import today, add_days, add_months

class TestMembership(FrappeTestCase):

    def test_membership_creation(self):
        membership = frappe.get_doc({
            'doctype': 'Membership',
            'member_name': 'Test Member',
            'expiry_date': '2024-12-31'
        })
        membership.insert()
        self.assertTrue(frappe.db.exists('Membership', membership.name))

    def test_expiry_date_validation(self):
        membership = frappe.get_doc({
            'doctype': 'Membership',
            'member_name': 'Test Member',
            'expiry_date': '2023-01-01'
        })

        with self.assertRaises(frappe.ValidationError):
            membership.insert()

    def test_auto_generate_membership_id(self):
        membership = frappe.get_doc({
            'doctype': 'Membership',
            'member_name': 'Test Member'
        })
        membership.insert()
        self.assertTrue(membership.membership_id)

    def test_extend_membership(self):
        membership = frappe.get_doc({
            'doctype': 'Membership',
            'member_name': 'Test Member',
            'expiry_date': today()
        })
        membership.insert()
        membership.extend_membership(3)

        self.assertEqual(membership.expiry_date, add_months(today(), 3))

    def test_expiry_notification(self):
        membership = frappe.get_doc({
            'doctype': 'Membership',
            'member_name': 'Test Member',
            'member_email': 'test@example.com',
            'expiry_date': add_days(today(), 7)
        })
        membership.insert()

        # Trigger the before_save hook manually
        membership.before_save()

        # Check the email queue for a notification email
        email = frappe.get_last_doc('Email Queue')
        self.assertIn("Membership Expiry Notification", email.subject)

    def test_cancel_membership(self):
        membership = frappe.get_doc({
            'doctype': 'Membership',
            'member_name': 'Test Member',
            'status': 'Active'
        })
        membership.insert()

        # Cancel the membership
        membership.cancellation_reason = "No longer needed"
        membership.cancel_membership()

        self.assertEqual(membership.status, 'Cancelled')


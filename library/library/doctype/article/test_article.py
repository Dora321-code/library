# Copyright (c) 2024, dorah and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase

class TestArticle(FrappeTestCase):

    def test_article_status_change(self):
        article = frappe.get_doc({
            'doctype': 'Article',
            'title': 'Draft Article',
            'content': 'This article is initially a draft.',
            'status': 'Draft'
        })
        article.insert()

        # Change status to Published
        article.status = 'Published'
        article.save()

        # Checking if the published_on date is set
        self.assertIsNotNone(article.published_on)

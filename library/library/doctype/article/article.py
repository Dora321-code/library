# Copyright (c) 2024, dorah and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator

class Article(WebsiteGenerator):
    def on_update(self):
        super().on_update()
        frappe.website.render.clear_cache(self.route)

    def get_context(self, context):
        context.parents = [{'route': '/articles', 'title': 'Articles'}]
        return context
    
    def before_save(self):
        if not self.published_on and self.status == 'Published':
            self.published_on = frappe.utils.now()

    def get_context(self, context):
        if self.status == 'Draft':
            context.show_draft_banner = True
        return context
    def get_list_context(context):
        context.title = 'All Articles'
        context.introduction = 'Here is our list of available articles articles!'
        context.no_breadcrumbs = False
        context.row_class = 'col-md-6'
        return context
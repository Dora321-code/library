// Copyright (c) 2024, dorah and contributors
// For license information, please see license.txt

frappe.ui.form.on("Article", {
	refresh(frm) {
		frm.add_custom_button(__('Create Book Review'), () => {
            frappe.new_doc('Book Review', {
                article: frm.doc.name
            });
        });
	

	},
	status(frm) {
        if (frm.doc.status === 'Published') {
            frappe.call({
                method: 'frappe.core.doctype.communication.email.make',
                args: {
                    recipients: frm.doc.author_email,
                    subject: `Your article "${frm.doc.title}" has been published`,
                    content: `Hello, your article titled "${frm.doc.title}" is now live!`,
                    communication_medium: 'Email',
                    send_email: 1
                }
            });
        }
		
}
});

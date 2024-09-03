// Copyright (c) 2024, dorah and contributors
// For license information, please see license.txt
frappe.ui.form.on("Library Membership", {
    refresh(frm) {
        if (frm.doc.reference_type && frm.doc.reference_name) {
            frm.add_custom_button(__(frm.doc.reference_name), () => {
                frappe.set_route("Form", frm.doc.reference_type, frm.doc.reference_name);
            });
        }
    }
});
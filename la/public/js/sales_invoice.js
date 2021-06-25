frappe.ui.form.on("Sales Invoice", {
  "refresh": function (frm) {
    make_item_rates_readonly(frm);
  },
  "taxes_and_charges": function (frm) {
    if (frm.doc.taxes_and_charges) {
      frappe.after_ajax(() =>
        setTimeout(() => {
          set_included_in_print_rate_for_taxes(frm);
        }, 300))
    }
  }
})

frappe.ui.form.on("Sales Taxes and Charges", {
  "charge_type": function (frm, cdt, cdn) {
    let row = locals[cdt][cdn]
    frappe.model.set_value(row.doctype, row.name, "included_in_print_rate", 1);
  }
})


function make_item_rates_readonly(frm) {
  var df = frappe.meta.get_docfield("Sales Invoice Item", "rate", frm.doc.name);
  df.read_only = frm.doc.is_return == 1 ? 1 : 0;
  frm.refresh_field("items")
}
function set_included_in_print_rate_for_taxes(frm) {
  for (let row of (frm.doc.taxes || [])) {
    frappe.model.set_value(row.doctype, row.name, "included_in_print_rate", 1);
  }
  frm.refresh_field("taxes")
}
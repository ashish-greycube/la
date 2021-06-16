frappe.ui.form.on('Material Request', {
  refresh: function (frm) {
    if (frm.custom_buttons[__('Transfer Material')] && frappe.user_roles.includes("System Manager") == false) {
      frappe.db.get_list('LA Warehouse User Permission', {
        fields: ['name'],
        filters: {
          user: frappe.user.name
        }
      }).then(records => {
        console.log(records);
        if (records.length > 0 && records[0].name) {} 
        else {
          frm.remove_custom_button(__('Transfer Material'), __('Create'))
          frappe.show_alert({
            message: __("For selected 'Set Source Warehouse' you donot have rights to do 'Transfer Material' action"),
            indicator: 'red'
          }, 10);
        }
      })
    }

  }
})
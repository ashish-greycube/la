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

  },
  mr_status_cf:function(frm){
    frm.events.add_custom_button_for_transit(frm)
  },
  update_mr_status_manually: function(frm){
    if (frm.doc.mr_status_cf=='Not Completed') {
      frm.set_value('mr_status_cf','Completed')
      frm.set_value('was_mr_status_set_manually_cf','1')
      frappe.show_alert({
        message: __("MR Status is updated to 'Completed'. 'Was MR Status Set Manually ?' is checked."),
        indicator: 'green'
      }, 10);      
      
    }else if(frm.doc.mr_status_cf=='Completed'){
      frm.set_value('mr_status_cf','Not Completed')
      frm.set_value('was_mr_status_set_manually_cf','1')
      frappe.show_alert({
        message: __("MR Status is updated to 'Not Completed'. 'Was MR Status Set Manually ?' is checked."),
        indicator: 'yellow'
      }, 10);          
    }
  },
  add_custom_button_for_transit: function(frm){
    frm.remove_custom_button('Complete Transit')
    frm.remove_custom_button('Reopen Transit')
    if (frm.doc.material_request_type == 'Material Transfer' && frm.doc.mr_status_cf=='Not Completed'){
			frm.add_custom_button(__("Complete Transit"),
				() => frm.events.update_mr_status_manually(frm));
    }else if(frm.doc.material_request_type == 'Material Transfer' && frm.doc.mr_status_cf=='Completed'){
			frm.add_custom_button(__("Reopen Transit"),
				() => frm.events.update_mr_status_manually(frm));
    }
  },
  onload_post_render:function(frm){
    frm.events.add_custom_button_for_transit(frm)
  }
})
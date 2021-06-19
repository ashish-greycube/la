import frappe
from frappe import _
from frappe.utils import get_url_to_form

def check_approvals_and_update_mr_status_based_on_completed_qty(self,method):
  check_approvals_on_submit_for_stock_entry(self,method)
  update_material_request_status_cf_based_on_completed_qty(self,method)

def check_approvals_on_submit_for_stock_entry(self,method):
  if method=='on_submit':
    if self.add_to_transit==1:
      if self.driver_receive_approval_cf==0:
        frappe.throw(
          msg=_("This stock entry is for 'Transit', so please check 'Driver Receive Approval' to continue with submit."),
          title=_('Driver Receive Approval is mandatory.'))
    elif self.outgoing_stock_entry and self.driver_delivery_approval_cf==0:
        frappe.throw(
          msg=_("This stock entry is for 'End Transit', so please check 'Driver Delivery Approval' to continue with submit."),
          title=_('Driver Delivery Approval is mandatory.'))

def check_approvals_on_save_for_stock_entry(self,method):          
  if method=='validate':
    if self.outgoing_stock_entry and self.receiver_approval_cf==0:
        frappe.throw(
          msg=_("This stock entry is for 'End Transit', so please check 'Receiver Approval' to continue with saving."),
          title=_('Receiver Approval is mandatory.'))  

def update_material_request_status_cf_based_on_completed_qty(self,method):
  if method=='on_submit' or method=='on_cancel':
    if self.purpose=='Material Transfer' and self.outgoing_stock_entry:
      processed_mr=[]
      for item in self.items:
        if item.material_request and item.material_request_item and item.material_request not in processed_mr:
          mr_outpt=update_mr_status_cf(item.material_request)
          if mr_outpt==True:
            processed_mr.append(item.material_request)

def update_mr_status_cf(mr_name):
  mr_obj = frappe.get_doc("Material Request", mr_name)
  if mr_obj.material_request_type=='Material Transfer' and (mr_obj.was_mr_status_set_manually_cf==None or mr_obj.was_mr_status_set_manually_cf==0):
    if len(mr_obj.items)>0:
      mr_status_cf='Completed'
      for item in mr_obj.items:
        if item.complete_qty!=item.ordered_qty:
          mr_status_cf='Not Completed'
    if mr_status_cf:
      mr_obj.mr_status_cf=mr_status_cf
      mr_obj.save(ignore_permissions=True)
      frappe.msgprint(_("MR Status is updated to {0} for {1} .".format(frappe.bold(mr_status_cf),get_url_to_form('Material Request',mr_name))),alert=True)
    return True
  else:
    return False

@frappe.whitelist()
def update_material_request_mr_status_manually(mr_name,mr_status_cf):
  frappe.db.set_value('Material Request', mr_name, {'mr_status_cf': mr_status_cf, 'was_mr_status_set_manually_cf':1})
  return
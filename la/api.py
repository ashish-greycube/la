import frappe
from frappe import _
from frappe.utils import get_url_to_form

def sales_invoice_custom_validation(self,method):
  # [A] restrict warehouse to user's pos profile
  # Allow user to see quantity from sales invoice but restrict him to sell from another warehouse (only warehouse linked to his profile in POS),
  # for admin (user with no POS profile) allow to sell from any warehouse
  if self.pos_profile:
    default_warehouse = frappe.db.get_value('POS Profile', self.pos_profile, 'warehouse')
    if default_warehouse:
      for item in self.items:
        if item.warehouse!=default_warehouse:
          frappe.throw(
            msg=_("Row : {0} has warehouse selected as {1}. Please use your default warehouse {2}".format(frappe.bold(item.idx),item.warehouse,frappe.bold(default_warehouse))),
            title=_('Incorrect warehouse.'))        
  
  # [B] fetch paid amount in payment table in sales invoice
  # When SI has is_pos = 1, after save, set doc.payments[0].amount  = outstanding_amount, also update the paid_amount field
  if self.is_pos==1 and self.outstanding_amount and self.payments:
    self.payments[0].amount=self.outstanding_amount
    self.run_method('set_paid_amount')
    frappe.msgprint(_("OUtstanding amount {0} is set in payments table: {1} mode of payment.".format(frappe.bold(self.payments[0].amount),
    frappe.bold(self.payments[0].mode_of_payment))),alert=True)

  # Don't allow User to edit rate in sales return 
  if self.is_return == 1 and self.return_against:
    for item in self.items:
      previous_sales_invoice_item=item.sales_invoice_item
      previous_rate=frappe.db.get_value('Sales Invoice Item', previous_sales_invoice_item, 'rate')
      if previous_rate != item.rate:
          frappe.throw(
            msg=_("Row : {0} has rate as {1}. It should be {2}. Please correct it to continue..".format(frappe.bold(item.idx),item.rate,frappe.bold(previous_rate))),
            title=_('Cannot edit rate for return item.'))          




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
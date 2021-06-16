import frappe
from frappe import _

def validate_approvals_for_stock_entry(self,method):
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

  elif method=='validate':
    if self.outgoing_stock_entry and self.receiver_approval_cf==0:
        frappe.throw(
          msg=_("This stock entry is for 'End Transit', so please check 'Receiver Approval' to continue with saving."),
          title=_('Receiver Approval is mandatory.'))
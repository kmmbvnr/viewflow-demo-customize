from viewflow import flow, lock
from viewflow.base import this, Flow

from . import views, models
from .helpers import task_owner


class ContractApprovalFlow(Flow):
    process_cls = models.ContractApprovalProcess
    lock_impl = lock.select_for_update_lock

    # Sales manager
    start = flow.Start(views.upload_contract) \
        .Permission('contract.can_upload_contract') \
        .Activate(this.split_approval)

    split_approval = flow.Split() \
        .Next(this.cfo_approval) \
        .Next(this.coo_approval)

    sign_contract = flow.View(views.sign_contract) \
        .Permission(task_owner(this.start)) \
        .Next(this.upload_contract)

    upload_contract = flow.View(views.upload_contract) \
        .Permission(task_owner(this.start)) \
        .Next(this.accounting_confirm)

    collect_pdc = flow.View(views.collect_pdc) \
        .Permission(task_owner(this.start)) \
        .Next(this.scan_pdc)

    # Chief Financial Officer
    cfo_approval = flow.View(views.cfo_approval) \
        .Permission('contract.can_cfo_approval') \
        .Next(this.check_cfo_remarks)

    check_cfo_remarks = flow.If(lambda p: p.cfo_remarks.exists()) \
        .OnTrue(this.join_approved) \
        .OnFalse(this.end_rejected)

    # Chief Operating Officer
    coo_approval = flow.View(views.coo_approval) \
        .Permission('contract.can_coo_approval') \
        .Next(this.check_coo_remarks)

    check_coo_remarks = flow.If(lambda p: p.coo_remarks.exists()) \
        .OnTrue(this.join_approved) \
        .OnFalse(this.end_rejected)

    join_approved = flow.Join() \
        .Next(this.sign_contract)

    # Accounting
    accounting_confirm = flow.View(views.accounting_confirm) \
        .Permission('contract.can_confirm_contract_data') \
        .Next(this.check_availability)

    post_rgr = flow.View(views.post_rgr) \
        .Permission('contract.can_post_rgr') \
        .Next(this.issue_invoice)

    confirm_remaining_payment = flow.View(views.confirm_remaining_payment) \
        .Permission('contract.can_confirm_remaining_payment') \
        .Next(this.deliver_equipment)

    post_sales_invoice = flow.View(views.post_sales_invoice) \
        .Permission('contract.can_post_sales_invoice') \
        .Next(this.collect_pdc)

    scan_pdc = flow.View(views.scan_pdc) \
        .Permission('contract.can_scan_pdc') \
        .Next(this.end)

    # Sales coordinator
    check_availability = flow.View(views.check_availability) \
        .Permission('contract.can_check_availability') \
        .Next(this.check_availability_if)

    check_availability_if = flow.If(lambda p: p.equipent_available()) \
        .OnTrue(this.allocate) \
        .OnFalse(this.issue_lpo)

    allocate = flow.View(views.allocate) \
        .Permission(task_owner(this.check_availability)) \
        .Next(this.issue_invoice)

    issue_invoice = flow.View(views.issue_invoice) \
        .Permission('contract.can_issue_sales_invoice') \
        .Next(confirm_remaining_payment)

    # Logistics
    issue_lpo = flow.View(views.issue_lpo) \
        .Permission('contract.can_issue_lpo') \
        .Next('equipment_received')

    equipment_received = flow.View(views.equipment_received) \
        .Permission('contract.can_notify_equipment_received') \
        .Next(this.upload_documents)

    upload_documents = flow.View(views.upload_documents) \
        .Permission(task_owner(this.equipment_received)) \
        .Next(this.post_rgr)

    deliver_equipment = flow.View(views.deliver_equipment) \
        .Permission('contract.can_deliver_equipment') \
        .Next(this.scan_delivery_note)

    scan_delivery_note = flow.View(views.scan_delivery_note) \
        .Permission(task_owner(this.deliver_equipment)) \
        .Next(this.post_sales_invoice)

    # End
    end_rejected = flow.End()
    end = flow.End()

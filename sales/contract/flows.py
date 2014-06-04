from viewflow import flow, lock
from viewflow.base import this, Flow

from . import views, models


class ContractApprovalFlow(Flow):
    process_cls = models.ApprovalProcess
    lock_impl = lock.select_for_update_lock

    # Sales manager
    start = flow.Start(views.AddContractView) \
        .Permission(auto_create=True) \
        .Activate(this.upload_contract)

    upload_contract = flow.View(views.UploadContractView) \
        .Assign(this.start.owner) \
        .Next(this.split_approval)

    split_approval = flow.Split() \
        .Next(this.cfo_approval) \
        .Next(this.coo_approval)

    sign_contract = flow.View(views.sign_contract) \
        .Assign(this.start.owner) \
        .Next(this.upload_contract_checks)

    upload_contract_checks = flow.View(views.sign_contract) \
        .Assign(this.start.owner) \
        .Next(this.accounting_confirm)

    collect_pdc = flow.View(views.collect_pdc) \
        .Assign(this.start.owner) \
        .Next(this.scan_pdc)

    # Chief Financial Officer
    cfo_approval = flow.View(views.CFOApprovalView) \
        .Permission(auto_create=True) \
        .Next(this.check_cfo_remarks)

    check_cfo_remarks = flow.If(lambda p: p.cfo_approved()) \
        .OnTrue(this.join_approved) \
        .OnFalse(this.end_rejected)

    # Chief Operating Officer
    coo_approval = flow.View(views.COOApprovalView) \
        .Permission(auto_create=True) \
        .Next(this.check_coo_remarks)

    check_coo_remarks = flow.If(lambda p: p.coo_approved()) \
        .OnTrue(this.join_approved) \
        .OnFalse(this.end_rejected)

    join_approved = flow.Join() \
        .Next(this.sign_contract)

    # Accounting
    accounting_confirm = flow.View(views.accounting_confirm) \
        .Permission(auto_create=True) \
        .Next(this.check_availability)

    post_rgr = flow.View(views.post_rgr) \
        .Permission(auto_create=True) \
        .Next(this.issue_invoice)

    confirm_remaining_payment = flow.View(views.confirm_remaining_payment) \
        .Permission(auto_create=True) \
        .Next(this.deliver_equipment)

    post_sales_invoice = flow.View(views.post_sales_invoice) \
        .Permission(auto_create=True) \
        .Next(this.collect_pdc)

    scan_pdc = flow.View(views.scan_pdc) \
        .Permission(auto_create=True) \
        .Next(this.end)

    # Sales coordinator
    check_availability = flow.View(views.check_availability) \
        .Permission(auto_create=True) \
        .Next(this.check_availability_if)

    check_availability_if = flow.If(lambda p: p.equipent_available()) \
        .OnTrue(this.allocate) \
        .OnFalse(this.issue_lpo)

    allocate = flow.View(views.allocate) \
        .Assign(this.check_availability.owner) \
        .Next(this.issue_invoice)

    issue_invoice = flow.View(views.issue_invoice) \
        .Permission(auto_create=True) \
        .Next(confirm_remaining_payment)

    # Logistics
    issue_lpo = flow.View(views.issue_lpo) \
        .Permission(auto_create=True) \
        .Next('equipment_received')

    equipment_received = flow.View(views.equipment_received) \
        .Permission(permission='can_notify_equipment_received', auto_create=True) \
        .Next(this.upload_documents)

    upload_documents = flow.View(views.upload_documents) \
        .Assign(this.equipment_received.owner) \
        .Next(this.post_rgr)

    deliver_equipment = flow.View(views.deliver_equipment) \
        .Permission(auto_create=True) \
        .Next(this.scan_delivery_note)

    scan_delivery_note = flow.View(views.scan_delivery_note) \
        .Assign(this.deliver_equipment.owner) \
        .Next(this.post_sales_invoice)

    # End
    end_rejected = flow.End()
    end = flow.End()

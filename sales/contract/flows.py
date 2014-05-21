from viewflow import flow, lock
from viewflow.base import this, Flow

from . import views, models


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

    sign_contract = flow.View() \
        .Permission('contract.can_sign_contract') \
        .Next(this.upload_signed)  # TODO Created_by

    collect_pdc = flow.View() \
        .Permission('contract.can_collect_contract') \
        .Next(this.scan_pdc)  # TODO Created_by

    # Chief Financial Officer
    cfo_approval = flow.View() \
        .Permission('contract.can_cfo_approval') \
        .Next(this.check_cfo_remarks)

    check_cfo_remarks = flow.If(lambda p: p.cfo_remarks.exists()) \
        .OnTrue(this.join_approved) \
        .OnFalse(this.end_rejected)

    # Chief Operating Officer
    coo_approval = flow.View() \
        .Permission('contract.can_coo_approval') \
        .Next(this.check_coo_remarks)

    check_coo_remarks = flow.If(lambda p: p.coo_remarks.exists()) \
        .OnTrue(this.join_approved) \
        .OnFalse(this.end_rejected)

    join_approved = flow.Join() \
        .Next(this.sign_contract)

    # Accounting
    accounting_confirm = flow.View() \
        .Permission('can_confirm_contract_data') \
        .Next('check_availability')

    post_pgr = flow.View() \
        .Next(this.issue_invoice)

    confirm_remaining_payment = flow.View() \
        .Next(this.deliver_equipment)

    post_sales_invoice = flow.View() \
        .Next(this.collect_pdc)

    scan_pdc = flow.View() \
        .Next(this.end)

    # Sales coordinator
    check_availability = flow.View() \
        .Permission(this.can_check_availability) \
        .Next(this.check_availability_if)

    check_availability_if = flow.If(lambda p: p.equipent_available()) \
        .OnTrue(this.allocate) \
        .OnFalse(this.issue_lpo)

    allocate = flow.View() \
        .Permission() \
        .Next(this.issue_invoice)

    issue_invoice = flow.View() \
        .Next(confirm_remaining_payment)

    # Logistics
    issue_lpo = flow.View() \
        .Next('equipment_received')

    equipment_received = flow.View() \
        .Next(this.upload_docuemnts)

    upload_docuemnts = flow.View() \
        .Next(this.confirm_receiving)

    confirm_receiving = flow.View() \
        .Next(this.post_pgr)

    deliver_equipment = flow.View() \
        .Next(this.scan_delivery_note)

    scan_delivery_note = flow.View() \
        .Next(this.post_sales_invoice)

    # End
    end_rejected = flow.End()
    end = flow.End()

from django.shortcuts import render


def index(request):
    """
    Home view
    """
    from .flows import ContractApprovalFlow

    has_start_permission = ContractApprovalFlow.start.has_perm(request.user)

    return render(request, 'index.html',
                  {'has_start_permission': has_start_permission})


def upload_contract(request, activation):
    pass


def sign_contract(request, activation):
    pass


def collect_pdc(request, activation):
    pass


def cfo_approval(request, activation):
    pass


def coo_approval(request, activation):
    pass


def accounting_confirm(request, activation):
    pass


def post_rgr(request, activation):
    pass


def confirm_remaining_payment(request, activation):
    pass


def post_sales_invoice(request, activation):
    pass


def scan_pdc(request, activation):
    pass


def check_availability(request, activation):
    pass


def allocate(request, activation):
    pass


def issue_invoice(request, activation):
    pass


def issue_lpo(request, activation):
    pass


def equipment_received(request, activation):
    pass


def upload_documents(request, activation):
    pass


def confirm_receiving(request, activation):
    pass


def deliver_equipment(request, activation):
    pass


def scan_delivery_note(request, activation):
    pass

from django import forms
from django.views.generic import CreateView, UpdateView, FormView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from viewflow.flow.start import StartViewMixin
from viewflow.flow.view import TaskViewMixin

from .models import Contract, ContractScan, ContractSubmission


@login_required
def index(request):
    """
    Home view
    """
    from .flows import ContractApprovalFlow
    has_start_permission = ContractApprovalFlow.start.has_perm(request.user)

    task_data = {
        'assigned': ContractApprovalFlow.task_cls.objects.filter(
            owner=request.user,
            status='NEW'),
        'unassigned': ContractApprovalFlow.task_cls.objects.filter(
            flow_task_type='VIEW',
            owner__isnull=True,
            status='NEW'),
        'equipment_wait': ContractApprovalFlow.task_cls.objects.filter(
            flow_task=ContractApprovalFlow.equipment_received,
            status='NEW')
    }

    # Task List
    active_filter = request.GET.get('filter', 'assigned')
    task_list = ContractApprovalFlow.task_cls.objects.none()
    if active_filter in task_data:
        task_list = task_data[active_filter]

    return render(request, 'index.html',
                  {'task_data': task_data,
                   'task_list': task_list,
                   'has_start_permission': has_start_permission})


class AddContractView(StartViewMixin, CreateView):
    model = Contract
    fields = ['client_name', 'contract_number']

    def activation_done(self, form):
        self.object = form.save()
        self.activation.process.contract = self.object
        self.activation.done()


class UploadContractView(TaskViewMixin, FormView):
    def get_form_class(self):
        class UploadContractForm(forms.Form):
            contract_draft = forms.FileField()
            quotation_draft = forms.FileField()

        return UploadContractForm

    def activation_done(self, form):
        # Save contact submittion
        contract_draft = ContractScan.objects.create(
            contract=self.activation.process.contract,
            scan_type=ContractScan.TYPE.CONTRACT_DRAFT,
            scan=form.cleaned_data['contract_draft'])

        quotation_draft = ContractScan.objects.create(
            contract=self.activation.process.contract,
            scan_type=ContractScan.TYPE.CONTRACT_DRAFT,
            scan=form.cleaned_data['quotation_draft'])

        ContractSubmission.objects.create(
            contract=self.activation.process.contract,
            contract_draft=contract_draft,
            quotation_draft=quotation_draft)

        self.activation.done()


def sign_contract(request, activation):
    pass


def collect_pdc(request, activation):
    pass


class CFOApprovalView(TaskViewMixin, UpdateView):
    fields = ['cfo_remarks', 'cfo_approved']

    def get_object(self, queryset=None):
        return self.activation.process.contract.contractsubmission_set.latest()


class COOApprovalView(TaskViewMixin, UpdateView):
    fields = ['coo_remarks', 'coo_approved']

    def get_object(self, queryset=None):
        return self.activation.process.contract.contractsubmission_set.latest()


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

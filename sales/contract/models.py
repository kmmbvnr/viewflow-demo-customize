from django.db import models
from django_fsm import FSMField, transition
from viewflow.models import Process


class Contract(models.Model):
    class STATUS:
        DRAFT = 'DRF'
        SIGNED = 'SGN'
        CONFIRMED = 'CNF'

    STATUS_CHOICES = ((STATUS.DRAFT, 'Draft'),
                      (STATUS.SIGNED, 'Signed'),
                      (STATUS.CONFIRMED, 'Confirmed'))

    status = FSMField(default=STATUS.DRAFT, choices=STATUS_CHOICES)
    process = models.ForeignKey('ContractApprovalProcess')

    cfo_remarks = models.TextField(blank=True, null=True)
    coo_remarks = models.TextField(blank=True, null=True)

    @transition(field=status, source=STATUS.DRAFT, target=STATUS.SIGNED,
                conditions=[lambda contract: contract.process.approved_contract_id is None])
    def sign(self):
        """
        Contract signed with customer
        """
        self.process.approved_contract = self
        self.process.save()

    @transition(field=status, source=STATUS.SIGNED, target=STATUS.CONFIRMED)
    def confirm(self):
        """
        Check confirmed
        """


class ContactScan(models.Model):
    class TYPE:
        CONTRACT_DRAFT = 'CONTRACT_DRAFT'
        QUOTATION_DRAFT = 'QUOTATION_DRAFT'
        CONTRACT_SIGNED = 'CONTRACT_SIGNED'
        CHECK = 'CHECK'
        POST_DATED_CHECH = 'PDC'

    TYPE_CHOICES = ((TYPE.CONTRACT_DRAFT, 'Contract draft'),
                    (TYPE.QUOTATION_DRAFT, 'Quotation draft'),
                    (TYPE.CONTRACT_SIGNED, 'Signed contract'),
                    (TYPE.CHECK, 'Check'),
                    (TYPE.POST_DATED_CHECH, 'Check'))

    contact = models.ForeignKey(Contract)
    scan_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    scan = models.FileField(upload_to='contracts/')


class ContractApprovalProcess(Process):
    client_name = models.CharField(max_length=250)
    contract_number = models.CharField(max_length=50)
    approved_contract = models.ForeignKey(Contract, null=True, blank=True)
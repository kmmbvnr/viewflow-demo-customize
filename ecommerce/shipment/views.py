from django.views import generic
from viewflow import flow

from . import models


class ShipmentView(flow.TaskFormViewMixin, generic.UpdateView):
    fields = []

    def get_object(self):
        return self.activation.process.shipment


class InsuranceView(flow.TaskFormViewMixin, generic.CreateView):
    model = models.Insurance
    fields = ['company_name', 'cost']

    def activation_done(self, form):
        self.object = form.save()

        shipment = self.activation.process.shipment
        shipment.insurance = self.object
        shipment.save(update_fields=['insurance'])

        self.activation.done()

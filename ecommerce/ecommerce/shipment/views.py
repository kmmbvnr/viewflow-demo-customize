from django.views import generic
from viewflow import views as flow_views

from . import models


class ShipmentView(flow_views.TaskViewMixin, generic.UpdateView):
    fields = []

    def get_object(self):
        return self.activation.process.shipment


class InsuranceView(flow_views.TaskViewMixin, generic.CreateView):
    model = models.Insurance
    fields = ['company_name', 'cost']

    def activation_done(self, form):
        self.object = form.save()

        shipment = self.activation.process.shipment
        shipment.insurance = self.object
        shipment.save(update_fields=['insurance'])

        self.activation.done()

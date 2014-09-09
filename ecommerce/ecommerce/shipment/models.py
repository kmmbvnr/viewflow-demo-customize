from django.db import models
from cartridge.shop.models import Order
from viewflow.models import Process


class Carrier(models.Model):
    DEFAULT = 'Default'

    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)

    def is_default(self):
        return self.name == Carrier.DEFAULT

    def __str__(self):
        return self.name


class Insurance(models.Model):
    company_name = models.CharField(max_length=50)
    cost = models.IntegerField()

    def __str__(self):
        return '{} ${}'.format(self.company_name, self.cost)


class Shipment(models.Model):
    carrier = models.ForeignKey(Carrier, null=True)
    order = models.ForeignKey(Order)

    need_insurance = models.BooleanField(default=False)
    insurance = models.ForeignKey('Insurance', null=True)

    carrier_quote = models.IntegerField(blank=True, default=0)
    post_label = models.TextField(blank=True, null=True)


class ShipmentProcess(Process):
    shipment = models.ForeignKey(Shipment)

    def is_normal_post(self):
        try:
            if self.shipment.carrier:
                return self.shipment.carrier.is_default()
            else:
                return None
        except (Shipment.DoesNotExist, Carrier.DoesNotExist):
            return None

    def need_extra_insurance(self):
        try:
            return self.shipment.need_insurance
        except Shipment.DoesNotExist:
            return None

    class Meta:
        verbose_name_plural = 'Shipment process list'

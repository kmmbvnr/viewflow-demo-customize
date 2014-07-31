from . import models


def start_shipment_process(activation, order):
    activation.prepare()

    shipment = models.Shipment(order=order)
    shipment.save()

    activation.process.shipment = shipment
    activation.done()

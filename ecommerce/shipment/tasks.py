from . import models


def start_shipment_process(activation, order):
    activation.prepare()

    shipment = models.Shipment(order=order)
    shipment.save()

    activation.process.shipment = shipment
    activation.done()


def done_order(activation):
    order = activation.process.shipment.order
    order.status = 2  # DONE
    order.save()

    activation.done()

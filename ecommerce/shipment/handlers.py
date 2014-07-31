from . import flows


def cartridge_order_handler(request, order_form, order):
    flows.ShipmentFlow.start.run(order)

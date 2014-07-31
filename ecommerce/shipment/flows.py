from viewflow import flow
from viewflow.base import this, Flow
from viewflow.views import ProcessView

from . import tasks, models
from . import views


class ShipmentFlow(Flow):
    """
    Delivery process
    """
    process_cls = models.ShipmentProcess

    start = flow.StartFunction(tasks.start_shipment_process) \
        .Next(this.split_clerk_warehouse)

    # clerk
    split_clerk_warehouse = flow.Split() \
        .Next(this.set_shipment_type) \
        .Next(this.package_goods)

    set_shipment_type = flow.View(views.ShipmentView, fields=["carrier"]) \
        .Permission(auto_create=True) \
        .Next(this.delivery_mode)

    delivery_mode = flow.If(cond=lambda p: p.is_normal_post()) \
        .OnTrue(this.check_insurance) \
        .OnFalse(this.request_quotes)

    request_quotes = flow.View(views.ShipmentView, fields=["carrier_quote"]) \
        .Assign(this.set_shipment_type.owner) \
        .Next(this.join_clerk_warehouse)

    check_insurance = flow.View(views.ShipmentView, fields=["need_insurance"]) \
        .Assign(this.set_shipment_type.owner) \
        .Next(this.split_on_insurance)

    split_on_insurance = flow.Split() \
        .Next(this.take_extra_insurance, cond=lambda p: p.need_extra_insurance()) \
        .Always(this.fill_post_label)

    fill_post_label = flow.View(views.ShipmentView, fields=["post_label"]) \
        .Next(this.join_on_insurance) \
        .Assign(this.set_shipment_type.owner)

    join_on_insurance = flow.Join() \
        .Next(this.join_clerk_warehouse)

    # Logistic manager
    take_extra_insurance = flow.View(views.InsuranceView) \
        .Next(this.join_on_insurance) \
        .Permission(auto_create=True)

    # Warehouse worker
    package_goods = flow.View(ProcessView) \
        .Next(this.join_clerk_warehouse) \
        .Permission(auto_create=True)

    join_clerk_warehouse = flow.Join() \
        .Next(this.move_package)

    move_package = flow.View(ProcessView.as_view()) \
        .Assign(this.package_goods.owner) \
        .Next(this.end)

    end = flow.End()

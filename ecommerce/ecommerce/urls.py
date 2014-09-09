from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from ecommerce.shipment.flows import ShipmentFlow

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url("^$", TemplateView.as_view(template_name="index.html"), name="home"),
    url(r'^admin/', include(admin.site.urls)),
    url("^shop/", include("cartridge.shop.urls")),
    url("^flow/", include(ShipmentFlow.instance.urls)),
    url("^account/orders/$", "cartridge.shop.views.order_history",
        name="shop_order_history"),

    ("^", include("mezzanine.urls")),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"

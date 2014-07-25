from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url("^$", "mezzanine.blog.views.blog_post_list", name="home"),

    url(r'^admin/', include(admin.site.urls)),
    url("^shop/", include("cartridge.shop.urls")),
    url("^account/orders/$", "cartridge.shop.views.order_history",
        name="shop_order_history"),

    ("^", include("mezzanine.urls")),
)

handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"

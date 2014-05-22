from django.conf.urls import patterns, include, url
from django.contrib import admin
from sales.contract.flows import ContractApprovalFlow

urlpatterns = patterns('',  # NOQA
    url(r'^$', 'sales.contract.views.index', name='index'),
    url(r'^contract/', include(ContractApprovalFlow.instance.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('sales.website'))
)

from django.conf.urls import patterns, include, url
from django.contrib import admin
from travel.request.flows import RequestFlow

urlpatterns = patterns('',  # NOQA
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(RequestFlow.instance.urls)),
    url(r'^', include('travel.website'))
)

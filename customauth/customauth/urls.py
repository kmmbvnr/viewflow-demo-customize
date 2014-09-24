from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView


urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^login/', TemplateView.as_view(template_name='login.html')),
    url(r'^parcel/', include('customauth.parcel.urls')),
    url(r'^', include('customauth.website')),
)

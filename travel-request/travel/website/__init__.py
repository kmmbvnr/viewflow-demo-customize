from django.conf.urls import patterns, url
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


def users(request):
    return {
        'users': User.objects.filter(is_active=True).order_by('-username')
    }


def login_as(request):
    user = request.REQUEST.get('user_pk', None)
    if user:
        try:
            user = User.objects.get(pk=user)
        except User.DoesNotExist:
            pass

    if user:
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return redirect('/')
    else:
        logout(request)
        return render(request, 'login.html')


urlpatterns = patterns('',  # NOQA
    url(r'^accounts/login/$', login_as, name="login"))

"""gitrec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from django.contrib.auth import login, logout
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,)
from django.contrib.auth import views as auth_views
	
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^recommendations/', include('recommendations.urls', namespace="recommendations")),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls', namespace="auth")),

    url(r'^accounts/change-password/$', auth_views.password_change, {'post_change_redirect': 'password_change_done'}, name='password_change'),
    url(r'^accounts/change-password-done/$', auth_views.password_change_done, name='password_change_done'),

    url(r'^accounts/password-reset/$', auth_views.password_reset, {'post_reset_redirect': 'password_reset_done'}, name='password_reset'),
    url(r'^accounts/password-reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^accounts/password-reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, {'post_reset_redirect' : 'password_reset_complete'}, name='password_reset_confirm'),
    url(r'^accounts/password-reset/complete/$', auth_views.password_reset_complete, name='password_reset_complete'),    
]


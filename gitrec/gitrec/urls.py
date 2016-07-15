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
from django.contrib.sitemaps.views import sitemap
# from recommendations.sitemaps import ReviewSitemap

from django.conf import settings
from django.conf.urls.static import static

# sitemaps = {'recommendations': ReviewSitemap,}

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^recommendations/', include('recommendations.urls', namespace="recommendations")),
    url(r'^accounts/', include('django.contrib.auth.urls', namespace="auth")),
    url(r'^accounts/', include('registration.backends.simple.urls')),
#    url(r'^account/', include('account.urls', namespace="account")),
#    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name="login")
]

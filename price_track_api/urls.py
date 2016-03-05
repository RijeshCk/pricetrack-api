"""price_track_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.authtoken import views
import api.views
import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^$', api.views.Endpoint.as_view()),
    url(r'^getall', api.views.GetallProducts.as_view()),
    url(r'^index', api.views.Index),
    url(r'^pricehistory/id=(?P<id>(\w+))',api.views.PriceHistory.as_view()),
    url(r'^login',api.views.Login.as_view()),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^GetsubscribedProducts',api.views.GetsubscribedProducts.as_view()),
    # url(r'^linkedin',api.views.Linkedin.as_view()),
    url(r'^LIlogin',api.views.linkedin_login)
]

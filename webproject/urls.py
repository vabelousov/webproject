# -*- coding:utf-8 -*-

"""webproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.generic import RedirectView
from django.conf.urls import url

from articles import views

# Добавьте URL соотношения, чтобы перенаправить запросы
# с корневового URL, на URL приложения
urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
     path('home/', include('articles.urls')),
]

urlpatterns += [
    path('', RedirectView.as_view(url='/home/', permanent=True)),
]

urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += [
    url(r'^signup/$', views.signup, name='signup'),
    url(
        r'^account_activation_sent/$',
        views.account_activation_sent,
        name='account_activation_sent'
    ),
    url(
        r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate,
        name='activate'
    ),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'^settings/$', views.settings, name='settings'),
    url(
        r'^settings/password/$',
        views.password,
        name='password'
    ),
]

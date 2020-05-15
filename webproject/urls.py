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
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from posts import views, sitemap as mysitemap

admin.autodiscover()

sitemaps = {
    'posts': mysitemap.PostSitemap,
}

# Добавьте URL соотношения, чтобы перенаправить запросы
# с корневового URL, на URL приложения
urlpatterns = [

    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
     path('home/', include('posts.urls')),
    prefix_default_language=False,
)


urlpatterns += i18n_patterns(
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.posts.sitemap'),
)

urlpatterns += i18n_patterns(
    path('', RedirectView.as_view(url='/home/', permanent=True)),
)

urlpatterns += static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

urlpatterns += i18n_patterns(
    path('accounts/', include('django.contrib.auth.urls')),
)

urlpatterns += i18n_patterns(
    path('signup/', views.signup, name='signup'),
    path(
        'account_activation_sent/',
        views.account_activation_sent,
        name='account_activation_sent'
    ),
    url(
        (
            r'^activate/'
            r'(?P<uidb64>[0-9A-Za-z_\-]+)/'
            r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/'
            r'$'
        ),
        views.activate,
        name='activate'
    ),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('settings/', views.settings, name='settings'),
    path(
        'settings/password/',
        views.password,
        name='password'
    ),
    url(
        r'^profile/(?P<username>\w+)/$',
        views.view_profile,
        name='view_profile'
    ),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('typo-graphica/', views.typo_graphica, name='typo-graphica'),
    path(
        'page_is_under_construction/',
        views.page_is_under_construction,
        name='under-construction'
    ),
    path(
        'site-statistics/',
        views.site_statistics,
        name='site-statistics'
    ),
)

# -*- coding:utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^articles/$', views.ArticleListView.as_view(),
        name='articles'),
    url(r'^topos/$', views.TopoListView.as_view(),
        name='topos'),
    url(r'^tips/$', views.TipListView.as_view(),
        name='tips'),
    url(r'^tours/$', views.TourListView.as_view(),
        name='tours'),
    url(r'^article/(?P<pk>\d+)$', views.ArticleDetailView.as_view(),
        name='article-detail'),
]

urlpatterns += [
    url(
        r'^myarticles/$',
        views.ArticlesByAuthorListView.as_view(),
        name='my-articles'
    ),
    url(
        r'^myarticle/create/$',
        views.ArticleCreate.as_view(),
        name='article_create'),
    url(
        r'^myarticle/(?P<pk>\d+)/update/$',
        views.ArticleUpdate.as_view(),
        name='article_update'
    ),
    url(
        r'^myarticle/(?P<pk>\d+)/delete/$',
        views.ArticleDelete.as_view(),
        name='article_delete'
    ),
]

# -*- coding:utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^articles/$', views.ArticleListView.as_view(), name='articles'),
    url(r'^topos/$', views.TopoListView.as_view(), name='topos'),
    url(r'^tips/$', views.TipListView.as_view(), name='tips'),
    url(r'^tours/$', views.TourListView.as_view(), name='tours'),
    url(
        r'^page/(?P<pk>\d+)$',
        views.ArticleDetailView.as_view(),
        name='article-detail'
    ),
    url(r'^gallery/$', views.ImagesListView.as_view(), name='gallery'),
    url(r'^image/(?P<pk>\d+)$', views.ImageView.as_view(), name='image'),
]

urlpatterns += [
    url(
        r'^mypages/$',
        views.ArticlesByAuthorListView.as_view(),
        name='my-articles'
    ),
    url(
        r'^myimages/$',
        views.ImagesByUserListView.as_view(),
        name='my-images'
    ),
    url(
        r'^myimage/(?P<pk>\d+)$',
        views.ImageDetailView.as_view(),
        name='image-view'
    ),
    url(
        r'^mypage/create/$',
        views.ArticleCreate.as_view(),
        name='article_create'
    ),
    url(
        r'^mypage/(?P<pk>\d+)/update/$',
        views.ArticleUpdate.as_view(),
        name='article_update'
    ),
    url(
        r'^mypage/(?P<pk>\d+)/delete/$',
        views.ArticleDelete.as_view(),
        name='article_delete'
    ),
    url(
        r'^myimage/create/$',
        views.ImageCreate.as_view(),
        name='image_create'),
    url(
        r'^myimage/(?P<pk>\d+)/update/$',
        views.ImageUpdate.as_view(),
        name='image_update'
    ),
    url(
        r'^myimage/(?P<pk>\d+)/delete/$',
        views.ImageDelete.as_view(),
        name='image_delete'
    ),
]

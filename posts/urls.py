# -*- coding:utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^outings/$', views.OutingListView.as_view(), name='outings'),
    url(r'^topos/$', views.TopoListView.as_view(), name='topos'),
    url(r'^tips/$', views.TipListView.as_view(), name='tips'),
    url(r'^albums/$', views.AlbumListView.as_view(), name='albums'),
    url(r'^common-images/$', views.CommonImageListView.as_view(), name='common-images'),
    url(
        r'^page/(?P<pk>\d+)$',
        views.PostDetailView.as_view(),
        name='post-detail'
    ),
    url(r'^image/(?P<pk>\d+)$', views.ImageView.as_view(), name='image'),
    url(r'^album/(?P<pk>\d+)$', views.AlbumDetailView.as_view(), name='album-view'),
]

urlpatterns += [
    url(
        r'^mypages/$',
        views.PostsByAuthorListView.as_view(),
        name='my-posts'
    ),
    url(
        r'^myalbums/$',
        views.AlbumsByAuthorListView.as_view(),
        name='my-albums'
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
        views.PostCreate.as_view(),
        name='post_create'
    ),
    url(
        r'^mypage/(?P<pk>\d+)/update/$',
        views.PostUpdate.as_view(),
        name='post_update'
    ),
    url(
        r'^mypage/(?P<pk>\d+)/delete/$',
        views.PostDelete.as_view(),
        name='post_delete'
    ),
    url(
        r'^myalbum/create/$',
        views.AlbumCreate.as_view(),
        name='album_create'),
    url(
        r'^myalbum/(?P<pk>\d+)/update/$',
        views.AlbumUpdate.as_view(),
        name='album_update'
    ),
    url(
        r'^myalbum/(?P<pk>\d+)/delete/$',
        views.AlbumDelete.as_view(),
        name='album_delete'
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

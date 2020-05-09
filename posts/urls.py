# -*- coding:utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^pages/(?P<type>\D+)/(?P<category>\D+)/$', views.PostListView.as_view(), name='pages'),
    url(r'^pages/(?P<type>\D+)/$', views.PostListView.as_view(), name='pages'),
    url(r'^pages/$', views.PostListView.as_view(), name='pages'),

    url(
        r'^page/(?P<pk>\d+)$',
        views.PostDetailView.as_view(),
        name='post-detail'
    ),
    url(r'^common-images/$', views.CommonImageListView.as_view(), name='common-images'),
    url('search/', views.post_search, name='post_search'),
    url(
        r'^page_is_under_construction/$',
        views.page_is_under_construction,
        name='under-construction'
    ),
]

urlpatterns += [
    url(
        r'^mypages/$',
        views.PostsByAuthorListView.as_view(),
        name='my-posts'
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
        r'^myimages/$',
        views.ImagesByUserListView.as_view(),
        name='my-images'
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

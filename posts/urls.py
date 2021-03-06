# -*- coding:utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(
        r'^pages/(?P<type>\D+)/(?P<category>\D+)/(?P<subcategory>\D+)/$',
        views.PostListView.as_view(),
        name='pages'
    ),
    url(
        r'^pages/(?P<type>\D+)/(?P<category>\D+)/$',
        views.PostListView.as_view(),
        name='pages'
    ),
    url(
        r'^pages/(?P<type>\D+)/$',
        views.PostListView.as_view(),
        name='pages'
    ),
    url(r'^pages/$', views.PostListView.as_view(), name='pages'),
    url(
        r'^page/(?P<slug>[-\w]+)/$',
        views.PostDetailView.as_view(),
        name='post-detail'
    ),
    url(
        r'^tagged-posts/(?P<slug>[-\w]+)/$',
        views.PostTagListView.as_view(),
        name="tagged-posts"
    ),
    url(
        r'^gallery/$',
        views.CommonImageListView.as_view(),
        name='common-images'
    ),
    url(
        r'^tagged-images/(?P<slug>[-\w]+)/$',
        views.ImageTagListView.as_view(),
        name="tagged-images"
    ),
    url('search/', views.post_search, name='post_search'),
    url(
        r'^mypages/$',
        views.PostsByAuthorListView.as_view(),
        name='my-posts'
    ),
    url(
        r'^user-tagged-posts/(?P<slug>[-\w]+)/$',
        views.UserPostTagListView.as_view(),
        name="user-tagged-posts"
    ),
    url(
        r'^mypage/create/$',
        views.PostCreate.as_view(),
        name='post_create'
    ),
    url(
        r'^mypage/(?P<slug>[-\w]+)/update/$',
        views.PostUpdate.as_view(),
        name='post_update'
    ),
    url(
        r'^mypage/(?P<slug>[-\w]+)/delete/$',
        views.PostDelete.as_view(),
        name='post_delete'
    ),
    url(
        r'^myimages/$',
        views.ImagesByUserListView.as_view(),
        name='my-images'
    ),
    url(
        r'^user-tagged-images/(?P<slug>[-\w]+)/$',
        views.UserImageTagListView.as_view(),
        name="user-tagged-images"
    ),
    url(
        r'^myimage/create/$',
        # views.ImageCreate.as_view(),
        views.multiple_images_upload,
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
    url(r'^contact-us/$', views.contact_us, name='contact-us'),
    url(r'^clear-basket/$', views.clear_basket, name='clear-basket'),
]

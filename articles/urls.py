from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^articles/$', views.ArticleListView.as_view(),
        name='articles'),
    url(r'^article/(?P<pk>\d+)$', views.ArticleDetailView.as_view(),
        name='article-detail'),
]

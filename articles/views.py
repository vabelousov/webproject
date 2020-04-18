from django.shortcuts import render
from django.views import generic

from .models import Article #, Image


def index(request):
    num_published_articles = Article.objects. \
        filter(status__exact='published').count()

    return render(
        request,
        'index.html',
        context={'num_published_articles': num_published_articles},
    )


class ArticleListView(generic.ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'articles/article_list.html'


class ArticleDetailView(generic.DetailView):
    model = Article
    # summary_image_url = Image.objects.all().count()
    # print(summary_image_url)

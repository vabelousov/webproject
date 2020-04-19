from django.shortcuts import render
from django.views import generic

from .models import Article, Image


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
    paginate_by = 3

    def get_queryset(self):
        return Article.objects.filter(status__exact='published')


class ArticleDetailView(generic.DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        '''
        ниже в цикле я заменяю все вхождения 
        условных кодов картинок на их пути
        '''
        for img in Image.objects.filter(article__exact=context['article'].id):
            context['article'].body = context['article'].body.replace(
                '[' + img.image_code + '_m]',
                img.image_middle_url
            )
            context['article'].body = context['article'].body.replace(
                '[' + img.image_code + '_o]',
                img.image_original_url
            )
        return context

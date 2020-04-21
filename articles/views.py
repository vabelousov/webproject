# -*- coding:utf-8 -*-
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Article, Image, Comment
from .forms import CommentForm, SignUpForm


def index(request):
    num_published_articles = Article.objects.filter(
        status__exact='published'
    ).count()
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


class ArticleDetailView(FormMixin, generic.DetailView):
    model = Article
    form_class = CommentForm

    def get_success_url(self):
        return reverse('article-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
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
        context['comments'] = Comment.objects.filter(
            comment_article__exact=context['article'].id
        ).filter(is_active=True)
        comment_form = CommentForm(
            initial={
                'comment_user': self.request.user,
                'comment_article': context['article'].id
            }
        )
        context['comment_form'] = comment_form
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(ArticleDetailView, self).form_valid(form)


class ArticlesByAuthorListView(LoginRequiredMixin, generic.ListView):
    model = Article
    template_name = 'articles/author_articles.html'
    paginate_by = 3

    def get_queryset(self):
        return Article.objects.filter(
            author=self.request.user
        ).filter(status__exact='published').order_by('-publish')


def signup(request):
    '''
    Вьюшка регистрации на сайте (с использованием профайла)
    используется Signal
    '''
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # load the profile instance created by the signal
            user.refresh_from_db()
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            #  user.is_superuser = True
            #  user.is_staff = True
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            print('form is not valid!!!!')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

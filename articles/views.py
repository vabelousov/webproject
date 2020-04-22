# -*- coding:utf-8 -*-
from django.db import transaction
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login  # authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.forms import AdminPasswordChangeForm,\
    PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from social_django.models import UserSocialAuth
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Article, Image, Comment, Profile
from .forms import CommentForm, SignUpForm, EditProfileForm,\
    ProfileForm, ArticleForm, ImagesFormSet
from .tokens import account_activation_token


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
        return Article.objects.filter(type__exact='article').\
            filter(status__exact='published')


class TopoListView(generic.ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'articles/article_list.html'
    paginate_by = 3

    def get_queryset(self):
        return Article.objects.filter(type__exact='topo').\
            filter(status__exact='published')


class TipListView(generic.ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'articles/article_list.html'
    paginate_by = 3

    def get_queryset(self):
        return Article.objects.filter(type__exact='tip').\
            filter(status__exact='published')


class TourListView(generic.ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'articles/article_list.html'
    paginate_by = 3

    def get_queryset(self):
        return Article.objects.filter(type__exact='tour').\
            filter(status__exact='published')


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
                str(img.get_middle_image())
            )
            context['article'].body = context['article'].body.replace(
                '[' + img.image_code + '_o]',
                str(img.get_orig_image())
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
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.filter(
            author=self.request.user
        ).order_by('type').order_by('-publish')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string(
                'account/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }
            )
            user.email_user(subject, message)
            return HttpResponseRedirect(reverse('account_activation_sent'))
        else:
            print('form is not valid!!!!')
    else:
        form = SignUpForm()
    return render(request, 'account/signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'account/account_activation_sent.html')


def activate(
        request,
        uidb64,
        token,
        backend='django.contrib.auth.backends.ModelBackend'
):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(
            request,
            user,
            backend='django.contrib.auth.backends.ModelBackend'
        )
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'account/account_activation_invalid.html')


@login_required
def settings(request):
    user = request.user

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (
            user.social_auth.count() > 1
            or user.has_usable_password()
    )

    return render(request, 'account/settings.html', {
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })


@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(
                request,
                'Your password was successfully updated!'
            )
            return redirect('settings')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'account/password.html', {'form': form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(
            request.POST,
            request.FILES,
            instance=request.user.profile
        )

        if form.is_valid() and profile_form.is_valid():
            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            return redirect('view_profile', username=request.user.username)
    else:
        form = EditProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        args = {}
        args['form'] = form
        args['profile_form'] = profile_form
        return render(request, 'account/edit_profile.html', args)


def view_profile(request, username):
    person_user = User.objects.get(username=username)
    person = Profile.objects.get(user=person_user)
    args = {}
    args['person'] = person
    args['person_user'] = person_user
    return render(request, 'account/view_profile.html', args)


class ArticleCreate(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(ArticleCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['article_images'] = ImagesFormSet(self.request.POST)
        else:
            data['article_images'] = ImagesFormSet()
        return data

    def get_initial(self, *args, **kwargs):
        initial = super(ArticleCreate, self).get_initial()
        initial.update(
            {
                'type': 'article',
                'status': 'draft',
                'author': self.request.user.id
            }
        )
        return initial

    def form_valid(self, form):
        context = self.get_context_data()
        article_images = context['article_images']
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if article_images.is_valid():
                article_images.instance = self.object
                article_images.save()
        return super(CreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('my-articles')


class ArticleUpdate(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(ArticleUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['article_images'] = ImagesFormSet(
                self.request.POST,
                instance=self.object
            )
        else:
            data['article_images'] = ImagesFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        article_images = context['article_images']
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if article_images.is_valid():
                article_images.instance = self.object
                article_images.save()
        return super(UpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('my-articles')


class ArticleDelete(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('my-articles')

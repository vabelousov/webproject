# -*- coding:utf-8 -*-
from django.utils.translation import gettext as _
from django.contrib.postgres.search import SearchVector
from django.template.context_processors import csrf
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
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

from .models import Post, Image, Comment, Profile, Carousel,\
    ImageBasket, Category, MyMenu, Type
from .forms import CommentForm, SignUpForm, EditProfileForm,\
    ProfileForm, PostForm, ImagesForm, SearchForm, UserImagesForm,\
    Comment2Form, ContactForm
from .tokens import account_activation_token
from django.core.mail import send_mail


def index(request):
    carousel = Carousel.objects.filter(
        is_active__exact=True
    ).order_by(
        'order'
    ).all()

    return render(
        request,
        'index.html',
        context={'carousel': carousel, },
    )


def page_is_under_construction(request):
    return render(request, 'page_is_under_construction.html', )


@login_required
def typo_graphica(request):
    return render(request, 'typographica.html', )


@login_required
def site_statistics(request):
    args = {}
    args['published_count'] = Post.published.count()
    args['draft_count'] = Post.draft.count()
    args['hidden_count'] = Post.hidden.count()
    args['comment_count'] = Comment.objects.count()
    args['inactive_comment_count'] = Comment.objects.filter(
        is_active__exact=False
    ).count()
    args['images_count'] = Image.objects.count()
    args['common_images_count'] = Image.objects.filter(
        common__exact=True
    ).count()
    args['carousel_count'] = Carousel.objects.count()
    args['category_count'] = Category.objects.count()
    args['type_count'] = Type.objects.count()
    args['menu_count'] = MyMenu.objects.count()
    return render(request, 'site-statistics.html', args)


class PostListView(generic.ListView):
    paginate_by = 9
    model = Post
    context_object_name = 'post_list'
    template_name = 'posts/post_list.html'

    def get_queryset(self):
        try:
            qs = Post.published.filter(
                type__code__exact=self.kwargs['type']
            ).filter(
                main_category__code__exact=self.kwargs['category']
            ).all()
        except:
            try:
                qs = Post.published.filter(
                    type__code__exact=self.kwargs['type']
                ).all()
            except:
                qs = Post.published.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['tags'] = Post.tags.all()
        return context


class PostTagListView(generic.ListView):
    paginate_by = 9
    model = Post
    context_object_name = 'post_list'
    template_name = 'posts/post_list.html'

    def get_queryset(self):
        try:
            qs = Post.published.filter(
                type__code__exact=self.kwargs['type']
            ).filter(
                main_category__code__exact=self.kwargs['category']
            ).filter(tags__slug=self.kwargs.get("slug")).all()
        except:
            try:
                qs = Post.published.filter(
                    type__code__exact=self.kwargs['type']
                ).filter(tags__slug=self.kwargs.get("slug")).all()
            except:
                qs = Post.published.filter(
                    tags__slug=self.kwargs.get("slug")
                ).all()
        return qs

    def get_context_data(self, **kwargs):
        context = super(PostTagListView, self).get_context_data(**kwargs)
        context["tag"] = Post.tags.get(slug=self.kwargs.get("slug")).name
        return context


class PostDetailView(FormMixin, generic.DetailView):
    model = Post
    form_class = CommentForm

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)

        context['comments'] = Comment.objects.filter(
            comment_post__exact=context['post'].id
        ).filter(is_active=True).order_by('-date_created')
        if self.request.user.is_authenticated:
            comment_form = CommentForm(
                initial={
                    'comment_user': self.request.user,
                    'comment_post': context['post'].id
                }
            )
        else:
            comment_form = Comment2Form(
                initial={
                    'comment_post': context['post'].id
                }
            )
        context['comment_form'] = comment_form
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user.is_authenticated:
            form = self.get_form(form_class=CommentForm)
        else:
            form = self.get_form(form_class=Comment2Form)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(PostDetailView, self).form_valid(form)


class PostsByAuthorListView(PermissionRequiredMixin, generic.ListView):
    permission_required = [
        'posts.add_post',
        'posts.change_post',
        'posts.delete_post'
    ]
    model = Post
    template_name = 'posts/user_posts.html'
    paginate_by = 30

    def get_queryset(self):
        return Post.objects.filter(
            author=self.request.user
        ).order_by('type__code').order_by('-date_published')


class CommonImageListView(generic.ListView):
    model = Image
    context_object_name = 'images_list'
    template_name = 'posts/image_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Image.objects.filter(common__exact=True)

    def get_context_data(self, **kwargs):
        context = super(CommonImageListView, self).get_context_data(**kwargs)
        img1 = []
        img2 = []
        img3 = []
        img4 = []
        i = 0
        all_img = context['images_list'].all()
        cnt = all_img.count()
        for img in all_img:
            if i % 4 == 0:
                img1.append(img)
            if i % 4 == 1:
                img2.append(img)
            if i % 4 == 2:
                img3.append(img)
            if i % 4 == 3:
                img4.append(img)
            i = i + 1
        context['common_images_1'] = img1
        context['common_images_2'] = img2
        context['common_images_3'] = img3
        context['common_images_4'] = img4
        context['img_count'] = cnt
        context['tags'] = Image.tags.all()
        return context


class ImageTagListView(generic.ListView):
    model = Image
    context_object_name = 'images_list'
    template_name = 'posts/image_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Image.objects.filter(
            common__exact=True
        ).filter(tags__slug=self.kwargs.get("slug")).all()

    def get_context_data(self, **kwargs):
        context = super(ImageTagListView, self).get_context_data(**kwargs)

        img1 = []
        img2 = []
        img3 = []
        img4 = []
        i = 0
        all_img = context['images_list'].all()
        cnt = all_img.count()
        for img in all_img:
            if i % 4 == 0:
                img1.append(img)
            if i % 4 == 1:
                img2.append(img)
            if i % 4 == 2:
                img3.append(img)
            if i % 4 == 3:
                img4.append(img)
            i = i + 1
        context['common_images_1'] = img1
        context['common_images_2'] = img2
        context['common_images_3'] = img3
        context['common_images_4'] = img4
        context['img_count'] = cnt

        context["tag"] = Image.tags.get(slug=self.kwargs.get("slug")).name
        return context


class ImagesByUserListView(PermissionRequiredMixin, generic.ListView):
    permission_required = [
        'posts.add_image',
        'posts.change_image',
        'posts.delete_image'
    ]
    model = Image
    form_class = UserImagesForm
    template_name = 'posts/user_images.html'
    paginate_by = 10

    def get_queryset(self):
        return Image.objects.filter(
            user=self.request.user
        )

    def post(self, request, *args, **kwargs):
        form = UserImagesForm(request.POST)
        if form.is_valid():
            if 'img-action' in request.POST:
                if 'delete-selected' in request.POST['img-action']:
                    if form.cleaned_data['image_object']:
                        for item in form.cleaned_data['image_object']:
                            item.delete()
                if 'clear-from-basket' in request.POST['img-action']:
                    if form.cleaned_data['image_object']:
                        for item in form.cleaned_data['image_object']:
                            try:
                                bsk = ImageBasket.objects.filter(
                                    user__exact=self.request.user
                                ).filter(image__id__exact=item.id).first()
                                bsk.delete()
                            except:
                                pass
                if 'add-to-basket' in request.POST['img-action']:
                    if form.cleaned_data['image_object']:
                        for item in form.cleaned_data['image_object']:
                            bsk = ImageBasket()
                            bsk.user = request.user
                            bsk.image = item
                            bsk.save()
        return HttpResponseRedirect('')


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
                _('Your password was successfully updated!')
            )
            return redirect('settings')
        else:
            messages.error(request, _('Please correct the error below.'))
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


def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                search=SearchVector('title', 'summary', 'body'),
            ).filter(search=query)

    paginator = Paginator(results, 5)
    page_number = request.GET.get('page')

    try:
        # Если существует, то выбираем эту страницу
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # Если None, то выбираем первую страницу
        page_obj = paginator.page(1)
    except EmptyPage:
        # Если вышли за последнюю страницу, то возвращаем последнюю
        page_obj = paginator.page(paginator.num_pages)

    args = {}
    args.update(csrf(request))
    args['form'] = form
    args['results'] = results
    args['page_obj'] = page_obj
    args['paginator'] = paginator
    args['query'] = query
    if page_obj:
        args['is_paginated'] = True
    return render(request, 'posts/search.html', args)


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'posts.add_post'
    model = Post
    form_class = PostForm
    success_url = None

    def get_initial(self, *args, **kwargs):
        initial = super(PostCreate, self).get_initial()
        initial.update(
            {
                # 'type': 'stories',
                'status': 'draft',
                'author': self.request.user.id
            }
        )
        return initial

    def get_success_url(self):
        return reverse_lazy('my-posts')


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'posts.change_post'
    model = Post
    form_class = PostForm
    success_url = None

    def get_success_url(self):
        return reverse_lazy('my-posts')

    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data(**kwargs)
        try:
            context['basket'] = ImageBasket.objects.filter(
                user__id__exact=self.request.user.id
            )
        except:
            pass
        return context


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'posts.delete_post'
    model = Post
    success_url = reverse_lazy('my-posts')

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Post, id=self.kwargs.get('pk'))
        obj.delete()
        return redirect('my-posts')


class ImageCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'posts.add_image'
    model = Image
    form_class = ImagesForm
    success_url = None

    def get_initial(self, *args, **kwargs):
        initial = super(ImageCreate, self).get_initial()
        initial.update(
            {
                'user': self.request.user.id
            }
        )
        return initial

    def get_success_url(self):
        return reverse_lazy('my-images')


class ImageUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'posts.change_image'
    model = Image
    form_class = ImagesForm
    success_url = None

    def get_success_url(self):
        return reverse_lazy('my-images')


class ImageDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'posts.delete_image'
    model = Image
    success_url = reverse_lazy('my-images')

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Image, id=self.kwargs.get('pk'))
        obj.delete()
        return redirect('my-images')


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            sender_name = form.cleaned_data['name']
            sender_email = form.cleaned_data['email']

            message = _('{0} has sent you a new message: \n\n{1}').\
                format(sender_name, form.cleaned_data['message'])
            send_mail(
                _('New Enquiry'),
                message,
                sender_email,
                ['enquiry@exampleco.com']
            )
            messages.add_message(
                request,
                messages.SUCCESS,
                _('Your message has been sent!')
            )
            return HttpResponseRedirect(
                ''
            )
    else:
        form = ContactForm()

    return render(request, 'posts/contact-us.html', {'form': form})

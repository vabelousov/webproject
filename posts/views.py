# -*- coding:utf-8 -*-
from django.contrib.postgres.search import SearchVector
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
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

from .models import Post, Image, Comment, Profile, Album
from .forms import CommentForm, SignUpForm, EditProfileForm,\
    ProfileForm, PostForm, ImagesForm, AlbumForm, SearchForm
from .tokens import account_activation_token


def index(request):
    num_published_outings = Post.objects.filter(
        status__exact='published'
    ).filter(
        type__exact='outing'
    ).count()
    num_published_topos = Post.objects.filter(
        status__exact='published'
    ).filter(
        type__exact='topo'
    ).count()
    num_published_tips = Post.objects.filter(
        status__exact='published'
    ).filter(
        type__exact='tip'
    ).count()
    num_published_albums = Album.objects.filter(
        type__exact='common'
    ).count()
    num_published_images = Image.objects.count()
    return render(
        request,
        'index.html',
        context={'num_published_outings': num_published_outings,
                 'num_published_topos': num_published_topos,
                 'num_published_tips': num_published_tips,
                 'num_published_albums': num_published_albums,
                 'num_published_images': num_published_images,
                 },
    )


class OutingListView(generic.ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'posts/post_list.html'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(
            type__exact='outing'
        ).filter(status__exact='published').order_by('-date_published')

    def get_context_data(self, **kwargs):
        context = super(OutingListView, self).get_context_data(**kwargs)
        context['list_name'] = 'Outings'
        return context


class TopoListView(generic.ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'posts/post_list.html'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(
            type__exact='topo'
        ).filter(status__exact='published').order_by('-date_published')

    def get_context_data(self, **kwargs):
        context = super(TopoListView, self).get_context_data(**kwargs)
        context['list_name'] = 'Topos'
        return context


class TipListView(generic.ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'posts/post_list.html'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(
            type__exact='tip'
        ).filter(status__exact='published').order_by('-date_published')

    def get_context_data(self, **kwargs):
        context = super(TipListView, self).get_context_data(**kwargs)
        context['list_name'] = 'Tips'
        return context


class AlbumListView(generic.ListView):
    model = Post
    context_object_name = 'album_list'
    template_name = 'posts/album_list.html'
    paginate_by = 3

    def get_queryset(self):
        return Album.objects.filter(
            type__exact='common'
        ).order_by('-date_created')

    def get_context_data(self, **kwargs):
        context = super(AlbumListView, self).get_context_data(**kwargs)
        context['list_name'] = 'Albums'
        return context


class AlbumDetailView(generic.DetailView):
    model = Album
    template_name = 'posts/album_view.html'

    def get_context_data(self, **kwargs):
        context = super(AlbumDetailView, self).get_context_data(**kwargs)
        img1 = []
        img2 = []
        img3 = []
        i = 0
        all_img = Image.objects.filter(
            album__exact=self.object.id
        ).order_by('-date_created')
        cnt = all_img.count()
        for img in all_img:
            if i % 3 == 0:
                img1.append(img)
            if i % 3 == 1:
                img2.append(img)
            if i % 3 == 2:
                img3.append(img)
            i = i + 1
        context['album_images_1'] = img1
        context['album_images_2'] = img2
        context['album_images_3'] = img3
        context['img_count'] = cnt
        return context


class PostDetailView(FormMixin, generic.DetailView):
    model = Post
    form_class = CommentForm

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        '''
        ниже в цикле я заменяю все вхождения
        условных кодов картинок на их пути
        '''
        try:
            for img in Image.objects.filter(
                    album__exact=Album.objects.get(post=self.object.id)
            ):
                context['post'].body = context['post'].body.replace(
                    '[' + img.__str__() + '_m]',
                    str(img.get_image())
                )
                context['post'].body = context['post'].body.replace(
                    '[' + img.__str__() + '_o]',
                    str(img.get_original())
                )
        except:
            pass
        context['comments'] = Comment.objects.filter(
            comment_post__exact=context['post'].id
        ).filter(is_active=True).order_by('-date_created')
        comment_form = CommentForm(
            initial={
                'comment_user': self.request.user,
                'comment_post': context['post'].id
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
        return super(PostDetailView, self).form_valid(form)


class PostsByAuthorListView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = 'posts/author_posts.html'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(
            author=self.request.user
        ).order_by('type').order_by('-date_published')


class AlbumsByAuthorListView(generic.ListView):
    model = Album
    template_name = 'posts/user_albums.html'
    paginate_by = 3

    def get_queryset(self):
        return Album.objects.filter(
            author__exact=self.request.user
        ).order_by('-date_created')


class CommonImageListView(generic.ListView):
    model = Image
    context_object_name = 'images_list'
    template_name = 'posts/image_list.html'
    paginate_by = 5

    def get_queryset(self):
        return Image.objects.filter(
            common__exact=True
        ).order_by('-date_created')

    def get_context_data(self, **kwargs):
        context = super(CommonImageListView, self).get_context_data(**kwargs)
        img1 = []
        img2 = []
        img3 = []
        i = 0
        all_img = Image.objects.filter(
            common__exact=True
        ).order_by('-date_created')
        cnt = all_img.count()
        for img in all_img:
            if i % 3 == 0:
                img1.append(img)
            if i % 3 == 1:
                img2.append(img)
            if i % 3 == 2:
                img3.append(img)
            i = i + 1
        context['common_images_1'] = img1
        context['common_images_2'] = img2
        context['common_images_3'] = img3
        context['img_count'] = cnt
        return context


class ImagesByUserListView(LoginRequiredMixin, generic.ListView):
    model = Image
    template_name = 'posts/user_images.html'
    paginate_by = 8

    def get_queryset(self):
        return Image.objects.filter(
            user=self.request.user
        ).order_by('-date_created')


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


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.annotate(
                search=SearchVector('title', 'summary', 'body'),
            ).filter(search=query)
    return render(request,
                  'posts/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    success_url = None

    def get_initial(self, *args, **kwargs):
        initial = super(PostCreate, self).get_initial()
        initial.update(
            {
                'type': 'article',
                'status': 'draft',
                'author': self.request.user.id
            }
        )
        return initial

    def get_success_url(self):
        return reverse_lazy('my-posts')


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = None

    def get_success_url(self):
        return reverse_lazy('my-posts')

    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data(**kwargs)
        try:
            context['album_images_count'] = Image.objects.filter(album__exact=self.object.id).count()
            context['post_images'] = Image.objects.filter(
                album__exact=Album.objects.get(post=self.object.id).id
            ).all()
        except:
            pass
        return context


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('my-posts')


class ImageCreate(LoginRequiredMixin, CreateView):
    model = Image
    form_class = ImagesForm
    success_url = None

    def get_initial(self, *args, **kwargs):
        initial = super(ImageCreate, self).get_initial()
        initial.update(
            {
                'user': self.request.user
            }
        )
        return initial

    def get_success_url(self):
        return reverse_lazy('my-images')


class ImageUpdate(LoginRequiredMixin, UpdateView):
    model = Image
    form_class = ImagesForm
    success_url = None

    def get_success_url(self):
        return reverse_lazy('my-images')


class ImageDelete(LoginRequiredMixin, DeleteView):
    model = Image
    success_url = reverse_lazy('my-images')


class ImageDetailView(LoginRequiredMixin, generic.DetailView):
    model = Image
    context_object_name = 'image_view'
    template_name = "posts/image_view.html"


class ImageView(generic.DetailView):
    model = Image
    context_object_name = 'image'
    template_name = "posts/image.html"


class AlbumCreate(LoginRequiredMixin, CreateView):
    model = Album
    form_class = AlbumForm
    success_url = None

    def get_initial(self, *args, **kwargs):
        initial = super(AlbumCreate, self).get_initial()
        initial.update(
            {
                'author': self.request.user,
                'type': 'private'
            }
        )
        return initial

    def get_success_url(self):
        return reverse_lazy('my-albums')


class AlbumUpdate(LoginRequiredMixin, UpdateView):
    model = Album
    form_class = AlbumForm
    success_url = None

    def get_success_url(self):
        return reverse_lazy('my-albums')


class AlbumDelete(LoginRequiredMixin, DeleteView):
    model = Album
    success_url = reverse_lazy('my-albums')

    def get_context_data(self, **kwargs):
        context = super(AlbumDelete, self).get_context_data(**kwargs)
        context['album_images_count'] = Image.objects.filter(album__exact=self.object.id).count()
        return context

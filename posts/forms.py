# -*- coding:utf-8 -*-
from django import forms
from django.utils.translation import gettext_lazy as _
from taggit.forms import TagWidget
from .models import Comment, Post, Image
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class PostForm(forms.ModelForm):
    class Meta(object):
        model = Post
        exclude = ('date_published', 'date_created', 'date_updated')
        widgets = {
            'author': forms.HiddenInput(),
            # 'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4}
            ),
            'body': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 20}
            ),
            'thumbnail_url': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'main_category': forms.Select(attrs={'class': 'form-control'}),
            'sub_category': forms.Select(attrs={'class': 'form-control'}),
            'tags': TagWidget(attrs={'class': 'form-control'}),
        }


class ImagesForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ()
        widgets = {
            'user': forms.HiddenInput(),
            'original': forms.ClearableFileInput(attrs={'multiple': True}),
            'alt_text': forms.TextInput(attrs={'class': 'form-control'}),
            'common': forms.CheckboxInput(
                attrs={'class': 'form-check-input'}
            ),
            'tags': TagWidget(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_post', 'comment_user', 'comment_text']
        widgets = {
            'comment_post': forms.HiddenInput(),
            'comment_user': forms.HiddenInput(),
            'comment_text': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 5}
            ),
        }


class Comment2Form(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_post', 'user_name', 'user_email', 'comment_text']
        widgets = {
            'comment_post': forms.HiddenInput(),
            'user_name': forms.TextInput(attrs={'class': 'form-control'}),
            'user_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'comment_text': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 5}
            ),
        }


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = (
            'email',
            'first_name',
            'last_name',
            'bio',
            'location',
            'birth_date',
            'language',
            'avatar'
        )
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control'}),
            'language': forms.Select(attrs={'class': 'form-control'}),
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text='Required. Email address',
        label=_('E-mail'),
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'password1',
            'password2',
        )
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'class': 'form-control'}
        )
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'form-control'}
        )


class SearchForm(forms.Form):
    query = forms.CharField(
        label=_('Query'),
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )


class UserImagesForm(forms.Form):
    image_object = forms.ModelMultipleChoiceField(
        queryset=Image.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label=_('Your Name:'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        label=_('Your message:')
    )


class AuthenticationRememberMeForm(AuthenticationForm):
    """
    Subclass of Django ``AuthenticationForm`` which adds a remember me
    checkbox.
    """
    remember_me = forms.BooleanField(label=_('Remember Me'), initial=False,
                                     required=False)

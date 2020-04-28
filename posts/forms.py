# -*- coding:utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Comment, Profile, Post, Image, Album


class PostForm(forms.ModelForm):
    class Meta(object):
        model = Post
        exclude = ('date_published', 'date_created', 'date_updated')
        widgets = {
            'author': forms.HiddenInput(),
            'title': forms.Textarea(attrs={'cols': 120, 'rows': 1}),
            'summary': forms.Textarea(attrs={'cols': 120, 'rows': 4}),
            'body': forms.Textarea(attrs={'cols': 120, 'rows': 20}),
        }


class AlbumForm(forms.ModelForm):
    class Meta(object):
        model = Album
        exclude = ('date_created', )
        widgets = {
            'author': forms.HiddenInput(),
            'title': forms.Textarea(attrs={'cols': 120, 'rows': 1}),
            'description': forms.Textarea(attrs={'cols': 120, 'rows': 4}),
        }

class ImagesForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ()
        widgets = {
            'user': forms.HiddenInput(),
            'alt_text': forms.Textarea(attrs={'cols': 100, 'rows': 1}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_post', 'comment_user', 'comment_text']
        widgets = {
            'comment_post': forms.HiddenInput(),
            'comment_user': forms.HiddenInput(),
            'comment_text': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date', 'avatar')


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name'
        )


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text='Required. Email address'
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )

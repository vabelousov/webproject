# -*- coding:utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Comment, Profile, Post, Image


class PostForm(forms.ModelForm):
    class Meta(object):
        model = Post
        exclude = ('date_published', 'date_created', 'date_updated')
        widgets = {
            'author': forms.HiddenInput(),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 20}),
            'thumbnail_url': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'main_category': forms.Select(attrs={'class': 'form-control'}),
            'sub_category': forms.Select(attrs={'class': 'form-control'}),
        }


class ImagesForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ()
        widgets = {
            'user': forms.HiddenInput(),
            'alt_text': forms.TextInput(attrs={'class': 'form-control'}),
            'common': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_post', 'comment_user', 'comment_text']
        widgets = {
            'comment_post': forms.HiddenInput(),
            'comment_user': forms.HiddenInput(),
            'comment_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date', 'avatar')
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control'}),
        }


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name'
        )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

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
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

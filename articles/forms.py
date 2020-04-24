# -*- coding:utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
# from crispy_forms import layout
# from crispy_forms.helper import FormHelper
# from django.shortcuts import render
# from django.template.loader import render_to_string

from .models import Comment, Profile, Article, Image


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_article', 'comment_user', 'comment_text']
        widgets = {
            'comment_article': forms.HiddenInput(),
            'comment_user': forms.HiddenInput(),
            'comment_text': forms.Textarea(attrs={'cols': 120, 'rows': 5}),
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text='Required. Inform a valid email address.'
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name'
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date', 'avatar')


class ArticleForm(forms.ModelForm):
    class Meta(object):
        model = Article
        exclude = ('publish', 'created', 'updated')
        widgets = {
            'author': forms.HiddenInput(),
            'title': forms.Textarea(attrs={'cols': 120, 'rows': 1}),
            'summary': forms.Textarea(attrs={'cols': 120, 'rows': 4}),
            'body': forms.Textarea(attrs={'cols': 120, 'rows': 20}),
        }


class ImagesForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ()
        widgets = {
            'user': forms.HiddenInput(),
            'image_code': forms.Textarea(attrs={'cols': 12, 'rows': 1}),
            'image_text': forms.Textarea(attrs={'cols': 100, 'rows': 1}),
        }


ImagesFormSet = inlineformset_factory(
    Article,
    Image,
    form=ImagesForm,
    fields=(
        'image_code',
        'image_text',
        'article',
        'user',
        'image',
        'article_head',
        'gallery'
    ),
    extra=1
)

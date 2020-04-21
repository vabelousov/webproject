# -*- coding:utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_article', 'comment_user', 'comment_text']
        widgets = {
            'comment_article': forms.HiddenInput(),
            'comment_user': forms.HiddenInput()
        }


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='Optional.'
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='Optional.'
    )
    email = forms.EmailField(
        max_length=254,
        help_text='Required. Inform a valid email address.'
    )
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'birth_date',
            'password1',
            'password2',
)

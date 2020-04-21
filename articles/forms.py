# -*- coding:utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Comment, Profile


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_article', 'comment_user', 'comment_text']
        widgets = {
            'comment_article': forms.HiddenInput(),
            'comment_user': forms.HiddenInput()
        }


class SignUpForm(UserCreationForm):
    # first_name = forms.CharField(
    #     max_length=30,
    #     required=False,
    #     help_text='Optional.'
    # )
    # last_name = forms.CharField(
    #     max_length=30,
    #     required=False,
    #     help_text='Optional.'
    # )
    # birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
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
            'email',
            'first_name',
            'last_name'
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date', 'avatar')

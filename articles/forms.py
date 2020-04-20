# -*- coding:utf-8 -*-
from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_article', 'comment_user', 'comment_text']
        widgets = {
            'comment_article': forms.HiddenInput(),
            'comment_user': forms.HiddenInput()
        }

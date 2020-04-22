# -*- coding:utf-8 -*-
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from crispy_forms import layout
from crispy_forms.helper import FormHelper
from django.shortcuts import render
from django.template.loader import render_to_string

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

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = layout.Layout(
            layout.Div(
                layout.Field('title'),
                layout.Field('author'),
                layout.Field('summary'),
                layout.Field('body'),
                layout.Field('type'),
                layout.Field('status'),
                layout.Fieldset('Add images',
                                Formset('article_images')
                                ),
                layout.HTML("<br>"),
                layout.ButtonHolder(layout.Submit('submit', 'save')),
            )
        )


class ImagesForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ()


ImagesFormSet = inlineformset_factory(
    Article,
    Image,
    form=ImagesForm,
    fields=[
        'image_code',
        'image_text',
        'article',
        'image_small',
        'image_middle',
        'image_orig',
        'article_head',
        'slideshow'
    ],
    extra=1
)


class Formset(layout.LayoutObject):
    template = "articles/formset.html"

    def __init__(self, formset_name_in_context, template=None):
        self.formset_name_in_context = formset_name_in_context
        self.fields = []
        if template:
            self.template = template

    def render(
            self,
            form,
            form_style,
            context,
            template_pack=layout.TEMPLATE_PACK
    ):
        formset = context[self.formset_name_in_context]
        return render_to_string(self.template, {'formset': formset})

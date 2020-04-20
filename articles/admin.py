# -*- coding:utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User
from .models import Article, Image, Comment


class ImageInline(admin.StackedInline):
    model = Image
    fields = [
        (
            'image_code', 'image_text',
            'image_small_url', 'image_middle_url',
            'image_original_url', 'article_head', 'slideshow'
        ),
    ]
    extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_author', 'status')
    list_filter = ('status', 'publish')
    fieldsets = (
        (None, {
            'fields': ('title', 'summary', 'body', 'author',)
        }),
        ('Publishing', {
            'fields': (('status', 'publish',),)
        }),
    )
    inlines = [ImageInline]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image_code', 'article', 'article_head', 'slideshow')
    list_filter = ('slideshow', 'article_head')
    fieldsets = (
        (None, {
            'fields': ('image_code', 'article',)
        }),
        ('Summary', {
            'fields': ('image_text', 'article_head', 'slideshow',)
        }),
        ('URLs', {
            'fields': (('image_small_url', 'image_middle_url', 'image_original_url',),)
        }),
    )


admin.site.unregister(User)


@admin.register(User)
class MyUserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_superuser',
        'is_active'
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_user', 'comment_article', 'date_created', 'is_active')
    list_filter = ('comment_user', 'comment_article', 'is_active', 'date_created')
    search_fields = ('comment_user', 'comment_text')


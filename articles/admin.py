from django.contrib import admin
from .models import Article, Image


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
    list_display = ('title', 'author', 'status')
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

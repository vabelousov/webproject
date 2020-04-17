from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status')
    list_filter = ('status', 'publish')
    fieldsets = (
        ('Menu', {
            'fields': ('title', 'pict_url',)
        }),
        ('Article', {
            'fields': ('summary', 'body', 'author',)
        }),
        ('Publishing', {
            'fields': (('status', 'publish', ), )
        }),
    )

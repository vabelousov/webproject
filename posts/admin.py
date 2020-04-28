# -*- coding:utf-8 -*-

from django.contrib import admin
from django.contrib.auth.models import User
from .models import Post, Image, Comment, Profile, Album


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'
    fields = (
        'avatar_tag',
        'avatar',
        'bio',
        'location',
        'birth_date',
        'email_confirmed'
    )
    readonly_fields = ['avatar_tag']  # Specify that this read only field


class ImageInline(admin.TabularInline):
    model = Image
    can_delete = False
    verbose_name_plural = 'Images'
    fk_name = 'album'
    fields = (
        'image_tag',
        'image',
        'alt_text',
        'thumbnail',
        'common',
        'user'
    )
    exclude = ('date_created', )
    readonly_fields = ['image_tag']
    extra = 0


class AlbumInline(admin.TabularInline):
    model = Album
    can_delete = False
    verbose_name_plural = 'Albums'
    fk_name = 'post'
    fields = (
        'title',
        'description',
        'type',
        'author'
    )
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [AlbumInline]
    list_display = ('title', 'display_author', 'type', 'status')
    list_filter = ('type', 'status', 'date_published')
    fieldsets = (
        (None, {
            'fields': ('title', 'summary', 'author', 'thumbnail_id',)
        }),
        ('Text', {
            'fields': ('body',)
        }),
        ('Publishing', {
            'fields': ('type', 'status', 'date_published',)
        })
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(PostAdmin, self).get_inline_instances(request, obj)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'alt_text', 'album', 'user', 'thumbnail', 'common')
    list_filter = ('user',)
    fieldsets = (
        (None, {
            'fields': ('user', 'album',)
        }),
        ('Summary', {
            'fields': ('alt_text', 'thumbnail', 'common',)
        }),
        ('Images', {
            'fields': ('image',)
        }),
    )
    exclude = ('date_created', )

    def image_tag(self, instance):
        return instance.image_tag()


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ('title', 'description', 'post', 'author', 'type')
    list_filter = ('author', 'type',)
    fieldsets = (
        (None, {
            'fields': ('author', 'post',)
        }),
        ('Summary', {
            'fields': ('title', 'description', 'type',)
        }),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(AlbumAdmin, self).get_inline_instances(request, obj)

    def image_tag(self, obj):
        return obj.image.image_tag()


class MyUserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline]
    list_display = (
        'avatar_tag',
        'username',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_superuser',
        'is_active',
        'get_location'
    )

    def get_location(self, instance):
        return instance.profile.location
    get_location.short_description = 'Location'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(MyUserAdmin, self).get_inline_instances(request, obj)

    def avatar_tag(self, obj):
        return obj.profile.avatar_tag()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'comment_user',
        'comment_post',
        'date_created',
        'is_active'
    )
    list_filter = (
        'comment_user',
        'comment_post',
        'is_active',
        'date_created'
    )
    search_fields = ('comment_user', 'comment_text')


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

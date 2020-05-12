# -*- coding:utf-8 -*-

from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from django.contrib.auth.models import User
from .models import Post, Image, Comment, Profile, \
    MyMenu, Carousel, Category, ImageBasket


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


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'display_author', 'type',
        'main_category', 'sub_category',
        'status'
    )
    list_filter = ('type',
                   'main_category', 'sub_category', 'status', 'date_published'
                   )
    fieldsets = (
        (None, {
            'fields': ('title', 'summary', 'author', 'thumbnail_url',)
        }),
        ('Text', {
            'fields': ('body',)
        }),
        ('Publishing', {
            'fields': (('type',
                        'main_category', 'sub_category',
                        ),
                       ('status', 'date_published',),)
        })
    )


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'alt_text', 'user', 'common')
    list_filter = ('user',)
    exclude = ('date_created', )

    def image_tag(self, instance):
        return instance.image_tag()


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


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = (
        'carousel_tag',
        'title',
        'alt_text',
        'is_active',
        'order'
    )
    list_filter = (
        'is_active',
    )

    def carousel_tag(self, instance):
        return instance.carousel_tag()


@admin.register(ImageBasket)
class ImageBasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'image')
    list_filter = ('user', 'image')


admin.site.register(
    MyMenu,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        'title',
        'name',
        'order',
    ),
    list_display_links=(
        'indented_title',
    ),
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    list_filter = ('code',)


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

# -*- coding:utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe


class Article(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    TYPE_CHOICES = (
        ('article', 'Article'),
        ('topo', 'Topo'),
        ('tip', 'Tip'),
        ('tour', 'Tour'),
    )
    title = models.CharField(
        max_length=200,
        help_text="Article title."
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        help_text="Article author (choose username).",
        null=True
    )
    summary = models.TextField(
        max_length=1000,
        help_text="Enter a brief description of the article."
    )
    body = models.TextField(
        help_text="Add an article here. Use html tags."
    )
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='article',
        help_text="Choose type of the article from the drop-list"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        help_text="Choose status of the article from the drop-list"
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article-detail', args=[str(self.id)])

    def get_head_image_url(self):
        try:
            url = Image.objects.get(article=self.id).image_small.url
        except (ValueError,):
            url = '/static/images/no-image.png'
        return url

    def display_author(self):
        return User.objects.get(username=self.author).first_name \
               + ', ' + User.objects.get(username=self.author).last_name

    display_author.short_description = 'Author'

    class Meta:
        ordering = ('-publish',)


class Image(models.Model):
    image_code = models.CharField(
        max_length=10,
        help_text="Add here code to use in the articles"
    )
    image_small = models.ImageField(
        upload_to='media/images/small',
        verbose_name='Small image',
        blank=True
    )
    image_middle = models.ImageField(
        upload_to='media/images/middle',
        verbose_name='Middle image',
        blank=True
    )
    image_orig = models.ImageField(
        upload_to='media/images/orig',
        verbose_name='Original image',
        blank=True
    )
    image_text = models.TextField(
        max_length=1000,
        help_text="Enter a brief description of the image."
    )
    article_head = models.BooleanField(
        help_text="Check this, if image is article's main image."
    )
    slideshow = models.BooleanField(
        help_text="Check this, if image is included in slideshow"
    )
    article = models.ForeignKey(
        "Article",
        on_delete=models.SET_NULL,
        help_text="Choose article for the image",
        null=True
    )

    def __str__(self):
        return self.image_code

    def get_small_image(self):
        try:
            url = self.image_small.url
        except(ValueError,):
            url = '/static/images/no-image.png'
        return url

    def get_middle_image(self):
        try:
            url = self.image_middle.url
        except(ValueError,):
            url = '/static/images/no-image.png'
        return url

    def get_orig_image(self):
        try:
            url = self.image_orig.url
        except(ValueError,):
            url = '/static/images/no-image.png'
        return url


class Comment(models.Model):
    comment_article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='articles',
        help_text='Comment on article',
        null=True
    )
    comment_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='users',
        help_text='User who posted this comment',
        null=True
    )
    comment_text = models.TextField(help_text='Add your comment here')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(
        default=True,
        help_text='Uncheck to deactivate comment'
    )

    class Meta:
        ordering = ('date_created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(
            self.comment_user,
            self.comment_article
        )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    bio = models.TextField(
        max_length=500,
        blank=True,
        help_text='Few words about you'
    )
    location = models.CharField(
        max_length=30,
        blank=True,
        help_text='Add your location e.g. Moscow'
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        help_text='Add your birthday here'
    )
    avatar = models.ImageField(
        upload_to='media/images/users',
        verbose_name='Avatar image',
        blank=True
    )

    def __str__(self):
        return self.user.username

    def get_avatar(self):
        try:
            url = self.avatar.url
        except(ValueError,):
            url = '/static/images/no-avatar.png'

        return url

    def avatar_tag(self):
        return mark_safe(
            '<img src="%s" width="50" height="50" />' % self.get_avatar()
        )

    avatar_tag.short_description = 'Avatar'

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


#class SiteMenu(models.Model):
#    menu_title = models.CharField(
#        max_length=30,
#        help_text="Menu item"
#    )
#    menu_descripion = models.CharField(
#        max_length=200,
#        help_text="Menu description"
#    )
#    parent_id =
#    article = models.ForeignKey(
#        Article,
#        on_delete=models.SET_NULL,
#        help_text="Article",
#        null=True
#    )
#
#    def __str__(self):
#       return self.menu_title
#
#    def get_parent(self):
#        return SiteMenu.objects.get(id=self.parent)

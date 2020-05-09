# -*- coding:utf-8 -*-
from io import BytesIO
import os

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from uuid import uuid4
from functools import partial

from django.core.files.base import ContentFile
from PIL import Image as Img


def _update_filename(instance, filename, path):
    upload_to = path
    ext = filename.split('.')[-1]
    # get filename
    if instance.id:
        filename = 'file_{}.{}'.format(
            instance.id,
            ext
        )
    else:
        # set filename as random string
        filename = 'file_{}.{}'.format(
            str(uuid4().hex)[:12],
            ext
        )
    # return the whole path to the file
    return os.path.join(upload_to, filename)


def path_file_resize(path):
    return partial(_update_filename, path=path)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset().filter(status='published')


class DraftManager(models.Manager):
    def get_queryset(self):
        return super(DraftManager, self).get_queryset().filter(status='draft')


class Category(models.Model):
    code = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Carousel(models.Model):
    image = models.ImageField(
        upload_to='media/images/carousel',
        verbose_name='Image',
        blank=True
    )
    alt_text = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=100, blank=True)
    reverse_url = models.CharField(
        max_length=200,
        blank=True,
        default='under_construction'
    )
    url_attr = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    text = models.TextField(
        max_length=1000,
        help_text="Image text",
        blank=True,
        null=True
    )
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_carousel(self):
        try:
            url = self.image.url
        except:
            url = '/static/images/no-image.png'
        return url

    def carousel_tag(self):
        return mark_safe(
            '<img src="%s" width="50" height="50" />' % self.get_carousel()
        )

    carousel_tag.short_description = 'Carousel'

    class Meta:
        verbose_name = 'Carousel'
        verbose_name_plural = 'Carouseles'


class Image(models.Model):
    original = models.ImageField(
        upload_to=path_file_resize('media/images/originals'),
        verbose_name='Original',
        blank=True
    )
    image = models.ImageField(
        upload_to=path_file_resize('media/images/middles'),
        verbose_name='Middle size',
        editable=False
    )
    thumbnail = models.ImageField(
        upload_to=path_file_resize('media/images/thumbnails'),
        verbose_name='Thumbnail',
        editable=False
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="Uploader",
        default=1,
    )
    alt_text = models.CharField(
        null=False,
        blank=True,
        max_length=255,
        help_text="Alt text"
    )
    common = models.BooleanField(
        help_text="Common image",
        default=False
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'img_' + str(self.id).zfill(8)

    def save(self, *args, **kwargs):
        """
        Make and save the thumbnail for the photo here.
        """
        if self.pk is None:
            if not self.make_thumbnail():
                raise Exception(
                    'Could not create thumbnail - is the file type valid?'
                )
            if not self.make_middle():
                raise Exception(
                    'Could not create middle size image - is the file type valid?'
                )
        super(Image, self).save(*args, **kwargs)

    def make_thumbnail(self):
        basewidth = 200

        img = Img.open(self.original)
        width_percent = (basewidth / float(img.size[0]))
        height_size = int((float(img.size[1]) * float(width_percent)))
        img = img.resize((basewidth, height_size), Img.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.original.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False    # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        img.save(temp_thumb, FTYPE, quantity=100)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.thumbnail.save(
            os.path.basename(thumb_filename),
            ContentFile(temp_thumb.read()),
            save=False
        )
        temp_thumb.close()

        return True

    def make_middle(self):
        basewidth = 800

        img = Img.open(self.original)

        exif = None
        if 'exif' in img.info:
            exif = img.info['exif']
        width_percent = (basewidth / float(img.size[0]))
        height_size = int((float(img.size[1]) * float(width_percent)))
        img = img.resize((basewidth, height_size), Img.ANTIALIAS)

        image_name, image_extension = os.path.splitext(self.original.name)
        image_extension = image_extension.lower()

        image_filename = image_name + '_middle' + image_extension

        if image_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif image_extension == '.gif':
            FTYPE = 'GIF'
        elif image_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False    # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_image = BytesIO()
        if exif:
            img.save(temp_image, format=FTYPE, exif=exif, quality=100)
        else:
            img.save(temp_image, format=FTYPE, quality=100)
        temp_image.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.image.save(
            os.path.basename(image_filename),
            ContentFile(temp_image.read()),
            save=False
        )
        temp_image.close()

        return True

    def get_image(self):
        try:
            url = self.image.url
        except:
            url = '/static/images/no-image.png'
        return url

    def get_original(self):
        try:
            url = self.original.url
        except:
            url = '/static/images/no-image.png'
        return url

    def get_thumbnail(self):
        try:
            url = self.thumbnail.url
        except:
            url = '/static/images/no-image.png'
        return url

    def image_tag(self):
        return mark_safe(
            '<img src="%s" width="50" height="50" />' % self.get_thumbnail()
        )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Image'
        verbose_name_plural = 'Images'


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('hidden', 'Hidden')
    )
    TYPE_CHOICES = (
        ('stories', 'Stories'),
        ('topos', 'Topos'),
        ('tips', 'Tips'),
        ('others', 'Others')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        help_text="Post author",
        null=True
    )
    title = models.CharField(
        max_length=200,
        help_text="Post title"
    )
    summary = models.TextField(
        max_length=1000,
        help_text="Post summary",
        blank=True,
        null=True
    )
    body = models.TextField(
        help_text="Post text (html tags allowed)",
        blank=True,
        null=True
    )
    thumbnail_url = models.CharField(
        max_length=500,
        help_text="Thumbnail url",
        blank=True
    )
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='outing',
        help_text="Post type"
    )
    main_category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        help_text="Main category",
        null=True,
        related_name='main_category'
    )
    sub_category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        help_text="Sub category",
        null=True,
        related_name='sub_category'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        help_text="Post status"
    )
    date_published = models.DateTimeField(default=timezone.now)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()  # Менеджер по умолчанию
    published = PublishedManager()  # Собственный менеджер
    draft = DraftManager()  # Собственный менеджер

    def __str__(self):
        return self.title

    def get_post_code(self):
        return 'pst_' + str(self.id).zfill(8)

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.id)])

    def get_thumbnail(self):
        if len(self.thumbnail_url) > 0:
            url = self.thumbnail_url
        else:
            url = '/static/images/no-image.png'
        return url

    def display_author(self):
        return User.objects.get(
            username=self.author
        ).first_name + ' ' + User.objects.get(
            username=self.author
        ).last_name

    display_author.short_description = 'Author'

    class Meta:
        ordering = ('-date_published',)
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class ImageBasket(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.post.title + '_' + str(self.image.id)


class Comment(models.Model):
    comment_post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text='Comments',
        null=True
    )
    comment_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='users',
        help_text='Comment user',
        null=True
    )
    comment_text = models.TextField(help_text='Comment text')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(
        default=True,
        help_text='Active comment'
    )

    def __str__(self):
        return 'Comment by {} on {}'.format(
            self.comment_user,
            self.comment_post
        )

    class Meta:
        ordering = ('date_created',)
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


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

    def save(self, *args, **kwargs):
        """
        Make and save the thumbnail for the photo here.
        """
        super(Profile, self).save(*args, **kwargs)

        if self.avatar:
            if not self.make_avatar():
                raise Exception(
                    'Could not create avatar - is the file type valid?'
                )

    def make_avatar(self):
        basewidth = 150
        height_size = 150
        try:
            img = Img.open(self.avatar)
            img.thumbnail((basewidth, height_size), Img.ANTIALIAS)
            img.save(self.avatar.name, format='JPEG', quality=100)
        except:
            return False
        return True

    def get_avatar(self):
        try:
            url = self.avatar.url
        except:
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


class MyMenu(MPTTModel):
    title = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    reverse_url = models.CharField(
        max_length=200,
        blank=True,
        default='under_construction'
    )
    url_attr = models.CharField(max_length=100, blank=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    order = models.CharField(max_length=3, default='000')

    class MPTTMeta:
        order_insertion_by = ['order']

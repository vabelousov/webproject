# -*- coding:utf-8 -*-
from io import BytesIO
import os

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from uuid import uuid4
from functools import partial

from django.utils.translation import gettext as _

from django.core.files.base import ContentFile
from PIL import Image as Img
from .ru_taggit import UnicodeTaggedItem


def listToString(s):
    # initialize an empty string
    str1 = ""

    # traverse in the string
    for ele in s:
        str1 += ele

        # return string
    return str1


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


class HiddenManager(models.Manager):
    def get_queryset(self):
        return super(
            HiddenManager, self
        ).get_queryset().filter(status='hidden')


class Type(models.Model):
    code = models.CharField(
        verbose_name=_('Code'),
        max_length=100,
        blank=True
    )
    description = models.CharField(
        verbose_name=_('Description'),
        max_length=100,
        blank=True
    )

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _('Type')
        verbose_name_plural = _('Types')


class Category(models.Model):
    code = models.CharField(
        verbose_name=_('Code'),
        max_length=100,
        blank=True
    )
    description = models.CharField(
        verbose_name=_('Description'),
        max_length=100,
        blank=True
    )

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Carousel(models.Model):
    image = models.ImageField(
        verbose_name=_('Image'),
        upload_to='media/images/carousel',
        blank=True
    )
    alt_text = models.CharField(
        verbose_name=_('Alt'),
        max_length=100,
        blank=True
    )
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=100,
        blank=True
    )
    reverse_url = models.CharField(
        verbose_name=_('reverse URL'),
        max_length=200,
        blank=True,
        default='under_construction'
    )
    url_attr = models.CharField(
        verbose_name=_('URL attr'),
        max_length=100,
        blank=True
    )
    is_active = models.BooleanField(verbose_name=_('Active'), default=True)
    text = models.TextField(
        verbose_name=_('Text'),
        max_length=1000,
        help_text="Image text",
        blank=True,
        null=True
    )
    order = models.IntegerField(verbose_name=_('Order'), default=0)

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

    carousel_tag.short_description = _('Carousel')

    class Meta:
        verbose_name = _('Carousel')
        verbose_name_plural = _('Carousels')


class Image(models.Model):
    original = models.ImageField(
        upload_to=path_file_resize('media/images/originals'),
        verbose_name=_('Original'),
        blank=True
    )
    image = models.ImageField(
        upload_to=path_file_resize('media/images/middles'),
        verbose_name=_('Middle size'),
        editable=False
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text=_('Uploader'),
        default=1,
        verbose_name=_('User')
    )
    alt_text = models.CharField(
        null=False,
        blank=True,
        max_length=255,
        help_text=_('Alt text'),
        verbose_name=_('Alt text')
    )
    common = models.BooleanField(
        help_text=_('Common image'),
        default=False,
        verbose_name=_('Common')
    )
    date_created = models.DateTimeField(auto_now_add=True)

    tags = TaggableManager(
        through=UnicodeTaggedItem,
        blank=True,
        help_text='Tags list.',
        verbose_name=_('Tags')
    )  # менеджер тэгов

    def __str__(self):
        return 'img_' + str(self.id).zfill(8)

    def save(self, *args, **kwargs):
        """
        Make and save the thumbnail and middle size for the photo here.
        """
        # if self.pk is None:
        if self.original:
            if not self.make_middle():
                raise Exception(
                    _('Could not create middle size\
                    image - is the file type valid?')
                )
        else:
            self.image.delete()
        super(Image, self).save(*args, **kwargs)

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

    def is_in_basket(self):
        bsk = None
        try:
            bsk = ImageBasket.objects.filter(
                user__exact=self.user
            ).filter(image__id__exact=self.id)
        except:
            pass
        return True if bsk else False

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

    def image_tag(self):
        return mark_safe(
            '<img src="%s" width="50" height="50" />' % self.get_image()
        )

    class Meta:
        ordering = ('-id',)
        verbose_name = _('Image')
        verbose_name_plural = _('Images')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', _('Draft')),
        ('published', _('Published')),
        ('hidden', _('Hidden'))
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        help_text=_('Post author'),
        null=True,
        verbose_name=_('Author')
    )
    title = models.CharField(
        max_length=200,
        help_text=_('Post title'),
        verbose_name=_('Post title')
    )
    summary = models.TextField(
        max_length=1000,
        help_text=_('Post summary'),
        blank=True,
        null=True,
        verbose_name=_('Post summary')
    )
    body = models.TextField(
        help_text=_('Post text (html tags allowed)'),
        blank=True,
        null=True,
        verbose_name=_('Post text')
    )
    thumbnail_url = models.CharField(
        max_length=500,
        help_text=_('Thumbnail url'),
        blank=True,
        verbose_name=_('Thumbnail URL')
    )
    type = models.ForeignKey(
        Type,
        on_delete=models.SET_NULL,
        help_text=_('Post type'),
        null=True,
        related_name='type',
        verbose_name=_('Post type')
    )
    main_category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        help_text=_('Main category'),
        null=True,
        related_name='main_category',
        verbose_name=_('Category')
    )
    sub_category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        help_text=_('Sub category'),
        null=True,
        related_name='sub_category',
        verbose_name=_('Sub Category')
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        help_text=_('Post status'),
        verbose_name=_('Post status')
    )
    date_published = models.DateTimeField(default=timezone.now)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()  # Менеджер по умолчанию
    published = PublishedManager()  # Собственный менеджер
    draft = DraftManager()  # Собственный менеджер
    hidden = HiddenManager()  # Собственный менеджер
    tags = TaggableManager(
        through=UnicodeTaggedItem,
        blank=True,
        help_text='Tags list.',
        verbose_name=_('Tags')
    )  # менеджер тэгов

    @staticmethod
    def _create_post_records(count=3, tp='stories', mc='alpinism', sc=''):
        from loremipsum import get_sentences
        for i in range(count):
            pst = Post()
            pst.title = tp.capitalize() + ' ' + mc.capitalize() + ' ' + str(i)
            pst.summary = listToString(get_sentences(3, True))
            pst.body = '<p>' + listToString(get_sentences(10, True)) + '</p>'
            pst.author = User.objects.get(username='vladimir')
            pst.status = 'published'
            pst.type = Type.objects.get(code=tp)
            pst.main_category = Category.objects.get(code=mc)
            pst.sub_category = Category.objects.get(code=sc)
            pst.thumbnail_url = 'file_63e871582a15.jpg'
            pst.save()

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

    display_author.short_description = _('Author')

    class Meta:
        ordering = (
            'type',
            'main_category',
            'sub_category',
            '-date_published',
        )
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')


# Post._create_post_records(5, 'stories', 'alpinism')
# Post._create_post_records(4, 'stories', 'multipitches')
# Post._create_post_records(7, 'stories', 'climbing')
# Post._create_post_records(12, 'topos', 'alpinism')
# Post._create_post_records(3, 'topos', 'multipitches')
# Post._create_post_records(2, 'topos', 'climbing')
# Post._create_post_records(3, 'tips', 'alpinism')
# Post._create_post_records(4, 'tips', 'adaptation')
# Post._create_post_records(5, 'tips', 'equipment')


class ImageBasket(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        verbose_name=_('User')
    )
    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        null=True,
        verbose_name=_('Image')
    )

    def __str__(self):
        return self.user.username + '_' + str(self.image.id)

    class Meta:
        verbose_name = _('Basket')
        verbose_name_plural = _('Baskets')


class Comment(models.Model):
    comment_post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text=_('Comments'),
        null=True,
        verbose_name=_('Post')
    )
    comment_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='users',
        help_text=_('Comment user'),
        blank=True,
        null=True,
        verbose_name=_('Commentator')
    )
    user_name = models.CharField(
        max_length=100,
        verbose_name=_('username'),
        null=True
    )
    user_email = models.EmailField(
        null=True,
        verbose_name=_('E-mail')
    )
    comment_text = models.TextField(
        help_text='Comment text',
        verbose_name=_('Comment')
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(
        default=True,
        help_text=_('Active comment'),
        verbose_name=_('Is active')
    )

    def __str__(self):
        return 'Comment by {} on {}'.format(
            self.comment_user,
            self.comment_post
        )

    class Meta:
        ordering = ('date_created',)
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('User')
    )
    email_confirmed = models.BooleanField(
        default=False,
        verbose_name=_('E-mail')
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        help_text=_('Few words about you'),
        verbose_name=_('BIO')
    )
    location = models.CharField(
        max_length=30,
        blank=True,
        help_text=_('Add your location e.g. Moscow'),
        verbose_name=_('Location')
    )
    birth_date = models.DateField(
        null=True,
        blank=True,
        help_text=_('Add your birthday here'),
        verbose_name=_('Birth date')
    )
    avatar = models.ImageField(
        upload_to='media/images/users',
        verbose_name=_('Avatar image'),
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
                    _('Could not create avatar - is the file type valid?')
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
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class MyMenu(MPTTModel):
    title = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('Title')
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_('Name')
    )
    reverse_url = models.CharField(
        max_length=200,
        blank=True,
        default='under_construction',
        verbose_name=_('Reverse url')
    )
    url_attr = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('URL attr')
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('Parent node')
    )
    order = models.CharField(
        max_length=3,
        default='000',
        verbose_name=_('Sort order')
    )
    active = models.BooleanField(verbose_name=_('Active node'), default=True)
    footer_node = models.BooleanField(
        verbose_name=_('Footer node'),
        default=False
    )

    class MPTTMeta:
        order_insertion_by = ['order']
        verbose_name = _('MyMenu')
        verbose_name_plural = _('MyMenus')

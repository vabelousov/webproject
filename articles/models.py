from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Article(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
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
    pict_url = models.ForeignKey(
        'Image',
        null=True,
        on_delete=models.SET_NULL,
        help_text="Add here image code to be used it article summary"
    )
    body = models.TextField(
        help_text="Add an article here. Use html tags."
    )
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        help_text="Choose the status of an article from the drop-list"
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article-detail', args=[str(self.id)])

    class Meta:
        ordering = ('-publish',)


class Image(models.Model):
    image_code = models.CharField(
        max_length=10,
        help_text="Add here code to use in articles"
    )
    image_small_url = models.URLField(
        help_text="Add here image small size url"
    )
    image_middle_url = models.URLField(
        help_text="Add here image middle size url"
    )
    image_original_url = models.URLField(
        help_text="Add here image original size url"
    )

    def __str__(self):
        return self

    def get_image_small_size_url_code(self):
        return self.image_code+'_s'

    def get_image_middle_size_url_code(self):
        return self.image_code+'_m'

    def get_image_original_size_url_code(self):
        return self.image_code+'_o'

    def get_image_small_size_url(self):
        return self.image_small_url

    def get_image_middle_size_url(self):
        return self.image_middle_url

    def get_image_original_size_url(self):
        return self.image_original_url

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
        on_delete=models.CASCADE,
        null=True,
        help_text="Article author (choose username)."
    )
    summary = models.TextField(
        max_length=1000,
        help_text="Enter a brief description of the article."
    )
    pict_url = models.TextField(
        max_length=1000,
        help_text="Add URL of the summary image."
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

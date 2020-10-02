from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from tinymce import HTMLField


class Category(models.Model):
    """Blog Post Categories."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Article(models.Model):
    """Blog Article posted by signed-in users."""
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=100, blank=False)
    headline = models.CharField(max_length=255, blank=False)
    pub_date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, default="General")
    body = HTMLField('Body Content')
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-pub_date', 'author', 'is_published']

    def __str__(self):
        return self.title

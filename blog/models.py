from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    """Blog Article posted by signed-in users."""
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(
        max_length=100, null=False,
        blank=False, unique=True)
    body = models.TextField(null=False, blank=False)
    image = models.ImageField(
        upload_to='blog/images/%Y/%m/',
        null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:150]

from django.contrib import admin
from .models import Article, Category


class ArticleAdmin(admin.ModelAdmin):
    model = Article
    exclude = ('author',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)

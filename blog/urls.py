from django.urls import path
from .views import (ArticleView, ArticleDetail)

app_name = 'blog'
urlpatterns = [
    path('articles/', ArticleView.as_view(), name='index'),
    path('articles/<pk>/', ArticleDetail.as_view(), name='article'),
]

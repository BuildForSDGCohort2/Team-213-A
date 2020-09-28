from django.urls import path
from .views import (ArticleView, ArticleDetail)

app_name = 'blog'
urlpatterns = [
    path('', ArticleView.as_view(), name='home'),
    path('<pk>/', ArticleDetail.as_view(), name='article')
]

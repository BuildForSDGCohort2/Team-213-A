from django.views.generic import ListView, DetailView
from .models import Article, Category


class ArticleView(ListView):
    """Shows a list and summary of all blogs."""
    queryset = Article.objects.order_by('-pub_date')
    template_name = 'blog/index.html'
    paginate_by = 3


class ArticleDetail(DetailView):
    """Displays individual blog posts/articles."""
    model = Article
    template_name = 'blog/article.html'

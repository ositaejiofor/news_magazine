from .models import Article, Category, BreakingNews
from .models import Tag


def global_context(request):
    return {
        "categories": Category.objects.all(),
        "featured_articles": Article.objects.filter(featured=True)[:5],
        "notifications": BreakingNews.objects.filter(is_active=True).order_by("-created_at")[:5],
    }


def news_globals(request):
    return {
        'get_all_categories': Category.objects.all(),
        'get_all_tags': Tag.objects.all(),
    }
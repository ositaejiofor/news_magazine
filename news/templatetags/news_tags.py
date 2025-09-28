# news/templatetags/news_tags.py
from django import template
from news.models import Category, Article

register = template.Library()

@register.simple_tag
def get_categories():
    """Return all categories."""
    return Category.objects.all().order_by("name")

@register.simple_tag
def get_featured_articles(limit=5):
    """Return 'limit' number of featured articles."""
    return Article.objects.filter(featured=True, status="published").order_by("-published_at")[:limit]

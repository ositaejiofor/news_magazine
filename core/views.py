# core/views.py
from django.shortcuts import render, get_object_or_404
from news.models import Article, Category, Tag, BreakingNews
from django.contrib.auth.decorators import login_required



@login_required
def dashboard_home(request):
    return render(request, "core/dashboard_home.html")


def home_view(request):
    latest_articles = Article.objects.order_by('-created_at')[:10]  # get latest 10 for flexibility
    return render(request, 'core/home.html', {
        'latest_articles': latest_articles
    })


# List all articles
# ----------------------------
def article_list(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'core/article_list.html', {'articles': articles})

# ----------------------------
# View single article detail
# ----------------------------
def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, "core/article_detail.html", {"article": article})

# ----------------------------
# View articles by category
# ----------------------------
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(category=category).order_by('-created_at')
    return render(request, 'core/category_detail.html', {'category': category, 'articles': articles})

# ----------------------------
# View articles by tag
# ----------------------------
def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    articles = Article.objects.filter(tags=tag).order_by('-created_at')
    return render(request, 'core/tag_detail.html', {'tag': tag, 'articles': articles})

# List all Breaking News
# ----------------------------
def breaking_news_list(request):
    breaking_news = BreakingNews.objects.all().order_by('-created_at')
    return render(request, 'core/breaking_news_list.html', {'breaking_news': breaking_news})


# ----------------------------
# View single Breaking News detail
# ----------------------------
def breaking_news_detail(request, slug):
    news_item = get_object_or_404(BreakingNews, slug=slug)
    return render(request, 'core/breaking_news_detail.html', {'news_item': news_item})
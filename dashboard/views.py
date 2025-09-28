from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from news.models import Article, BreakingNews
from news.models import Comment
from news.forms import ArticleForm

# ----------------------------
# ACCESS CONTROL DECORATORS
# ----------------------------

def superuser_required(view_func):
    """Restrict access to superusers only."""
    return user_passes_test(lambda u: u.is_superuser)(view_func)

def staff_required(view_func):
    """Restrict access to staff users only."""
    return user_passes_test(lambda u: u.is_staff)(view_func)

# ----------------------------
# DASHBOARD
# ----------------------------
@superuser_required
def dashboard_view(request):
    return render(request, "dashboard/dashboard.html")

# ----------------------------
# ARTICLE MANAGEMENT
# ----------------------------
@login_required
@staff_required
def manage_articles(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'dashboard/manage_articles.html', {'articles': articles})

@login_required
@staff_required
def add_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Article added successfully.")
            return redirect('dashboard:manage_articles')
    else:
        form = ArticleForm()
    return render(request, 'dashboard/article_form.html', {'form': form})

@login_required
@staff_required
def edit_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, "Article updated successfully.")
            return redirect('dashboard:manage_articles')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'dashboard/article_form.html', {'form': form})

@login_required
@staff_required
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        article.delete()
        messages.success(request, "Article deleted successfully.")
        return redirect('dashboard:manage_articles')
    return render(request, 'dashboard/delete_article.html', {'article': article})

# ----------------------------
# COMMENT MANAGEMENT
# ----------------------------
@login_required
@staff_required
def manage_comments(request):
    comments = Comment.objects.all().order_by('-created_at')
    return render(request, 'dashboard/manage_comments.html', {'comments': comments})

@login_required
@staff_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == "POST":
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
        return redirect('dashboard:manage_comments')
    return render(request, 'dashboard/delete_comment.html', {'comment': comment})

# ----------------------------
# BREAKING NEWS MANAGEMENT
# ----------------------------
@login_required
@staff_required
def manage_breaking_news(request):
    breaking_news = BreakingNews.objects.all().order_by('-created_at')
    return render(request, 'dashboard/manage_breaking_news.html', {'breaking_news': breaking_news})

@login_required
@staff_required
def add_breaking_news(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if title and content:
            BreakingNews.objects.create(title=title, content=content)
            messages.success(request, "Breaking news added successfully.")
            return redirect('dashboard:manage_breaking_news')
    return render(request, 'dashboard/add_breaking_news.html')

@login_required
@staff_required
def edit_breaking_news(request, pk):
    news_item = get_object_or_404(BreakingNews, pk=pk)
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if title and content:
            news_item.title = title
            news_item.content = content
            news_item.save()
            messages.success(request, "Breaking news updated successfully.")
            return redirect('dashboard:manage_breaking_news')
    return render(request, 'dashboard/edit_breaking_news.html', {'news_item': news_item})

@login_required
@staff_required
def delete_breaking_news(request, pk):
    news_item = get_object_or_404(BreakingNews, pk=pk)
    if request.method == "POST":
        news_item.delete()
        messages.success(request, "Breaking news deleted successfully.")
        return redirect('dashboard:manage_breaking_news')
    return render(request, 'dashboard/delete_breaking_news.html', {'news_item': news_item})

# ----------------------------
# ANALYTICS
# ----------------------------
@login_required
@staff_required
def analytics_view(request):
    total_articles = Article.objects.count()
    total_comments = Comment.objects.count()
    total_breaking_news = BreakingNews.objects.count()
    return render(request, "dashboard/analytics.html", {
        'total_articles': total_articles,
        'total_comments': total_comments,
        'total_breaking_news': total_breaking_news,
    })

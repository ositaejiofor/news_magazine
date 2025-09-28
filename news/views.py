from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Article, BreakingNews, Category, Tag, Comment
from .forms import ArticleForm, CommentForm, ReplyForm
from django.http import HttpResponse, HttpResponseBadRequest  # ✅ add this
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



# -------------------------------
# Public Views
# -------------------------------

def home_view(request):
    """Home page with featured and latest articles."""
    featured_articles = Article.objects.filter(
        status="published", featured=True
    ).order_by("-published_at")[:5]

    latest_articles = Article.objects.filter(
        status="published"
    ).order_by("-published_at")[:10]

    categories = Category.objects.all()

    return render(request, "news/home.html", {
        "featured_articles": featured_articles,
        "latest_articles": latest_articles,
        "categories": categories,
    })


def article_list_view(request):
    """List all published articles with pagination."""
    articles = Article.objects.filter(status="published").order_by("-published_at")
    paginator = Paginator(articles, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    featured_articles = Article.objects.filter(
        status="published", featured=True
    ).order_by("-published_at")[:5]

    return render(request, "news/article_list.html", {
        "articles": page_obj,
        "featured_articles": featured_articles,
    })


def article_detail_view(request, slug):
    """Show details of a single article with comments & replies."""
    article = get_object_or_404(Article, slug=slug, status="published")
    comments = article.comments.filter(parent__isnull=True).order_by("-created_at")

    # Forms
    comment_form = CommentForm()
    reply_form = ReplyForm()

    if request.method == "POST":
        if "parent_id" in request.POST:  # Reply
            reply_form = ReplyForm(request.POST)
            if reply_form.is_valid() and request.user.is_authenticated:
                parent_id = request.POST.get("parent_id")
                parent_comment = get_object_or_404(Comment, id=parent_id)
                reply = reply_form.save(commit=False)
                reply.article = article
                reply.user = request.user
                reply.parent = parent_comment
                reply.save()
                return redirect("news:article_detail", slug=article.slug)
        else:  # New comment
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid() and request.user.is_authenticated:
                comment = comment_form.save(commit=False)
                comment.article = article
                comment.user = request.user
                comment.save()
                return redirect("news:article_detail", slug=article.slug)

    # Related articles in the same category
    related_articles = Article.objects.filter(
        category=article.category,
        status="published"
    ).exclude(id=article.id).order_by("-published_at")[:4]

    return render(request, "news/article_detail.html", {
        "article": article,
        "related_articles": related_articles,
        "comments": comments,
        "comment_form": comment_form,
        "reply_form": reply_form,
    })


def category_detail_view(request, pk):
    """Display all articles for a specific category with pagination."""
    category = get_object_or_404(Category, pk=pk)
    articles = Article.objects.filter(
        category=category, status="published"
    ).order_by("-published_at")

    paginator = Paginator(articles, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "news/category_detail.html", {
        "category": category,
        "articles": page_obj,
    })


def tag_detail_view(request, slug):
    """Display all articles for a specific tag with pagination."""
    tag = get_object_or_404(Tag, slug=slug)
    articles = Article.objects.filter(
        tags=tag, status="published"
    ).order_by("-published_at")

    paginator = Paginator(articles, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "news/tag_detail.html", {
        "tag": tag,
        "articles": page_obj,
    })


# -------------------------------
# Breaking News Views
# -------------------------------

@staff_member_required
def breakingnews_list(request):
    """Staff-only list of breaking news."""
    breaking_news = BreakingNews.objects.all().order_by("-created_at")
    return render(request, "news/breakingnews_list.html", {"breaking_news": breaking_news})


@staff_member_required
def breakingnews_detail(request, slug):
    """Staff-only breaking news detail view."""
    news_item = get_object_or_404(BreakingNews, slug=slug)
    return render(request, "news/breakingnews_detail.html", {"news_item": news_item})


def public_breakingnews_list(request):
    """Public breaking news feed."""
    breaking_news = BreakingNews.objects.filter(active=True).order_by("-created_at")[:10]
    return render(request, "news/public_breakingnews_list.html", {"breaking_news": breaking_news})


def public_breakingnews_detail(request, slug):
    """Public breaking news detail view."""
    news_item = get_object_or_404(BreakingNews, slug=slug, active=True)
    return render(request, "news/public_breakingnews_detail.html", {"news_item": news_item})


# -------------------------------
# Optional: Article creation (for staff)
# -------------------------------

@staff_member_required
def add_article(request):
    """Staff can add a new article."""
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("dashboard_home")  # update to your dashboard URL
    else:
        form = ArticleForm()
    return render(request, "news/add_article.html", {"form": form})


@login_required
def add_comment(request, slug):
    """Handle AJAX comment/reply submissions via HTMX."""
    if request.method == "POST":
        article = get_object_or_404(Article, slug=slug, status="published")
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.article = article

            parent_id = request.POST.get("parent_id")
            if parent_id:
                try:
                    parent = Comment.objects.get(id=parent_id, article=article)
                    comment.parent = parent
                except Comment.DoesNotExist:
                    return HttpResponseBadRequest("Invalid parent comment")

            comment.save()

            # Decide which partial to render (comment vs reply)
            if comment.parent:
                html = render_to_string("news/_reply.html", {"reply": comment, "user": request.user})
            else:
                html = render_to_string("news/_comment.html", {"comment": comment, "user": request.user, "form": CommentForm()})

            return HttpResponse(html)

        return HttpResponseBadRequest("Invalid form")
    return HttpResponseBadRequest("Invalid request")

@login_required
@csrf_exempt
def ajax_post_comment(request):
    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user

            # Handle reply (parent)
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent_id = int(parent_id)

            comment.save()

            return JsonResponse({
                'success': True,
                'username': comment.user.username,
                'content': comment.content,
                'created_at': comment.created_at.strftime("%b %d, %Y %H:%M"),
                'comment_id': comment.id,
                'parent_id': comment.parent_id
            })
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
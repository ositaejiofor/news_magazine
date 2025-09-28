from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    # ----------- Breaking News (Public) -----------
    path("breaking-news/", views.public_breakingnews_list, name="public_breakingnews_list"),
    path("breaking-news/<slug:slug>/", views.public_breakingnews_detail, name="public_breakingnews_detail"),
    path("<slug:slug>/add-comment/", views.add_comment, name="add_comment"),

    # ----------- Breaking News (Staff Only) -----------
    path("staff/breaking-news/", views.breakingnews_list, name="breakingnews_list"),
    path("staff/breaking-news/<slug:slug>/", views.breakingnews_detail, name="breakingnews_detail"),

    # ----------- Categories -----------
    path("category/<int:pk>/", views.category_detail_view, name="category_detail"),

    # ----------- Tags -----------
    path("tag/<slug:slug>/", views.tag_detail_view, name="tag_detail"),

    # ----------- Articles -----------
    path("", views.article_list_view, name="article_list"),  # Main articles page
    path("<slug:slug>/", views.article_detail_view, name="article_detail"),  # Article detail

    path('ajax/post-comment/', views.ajax_post_comment, name='ajax_post_comment'),
]

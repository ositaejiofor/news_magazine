from django.urls import path
from . import views  # import views from dashboard app

app_name = "dashboard"

urlpatterns = [
    # Use the correct view name
    path("", views.dashboard_view, name="dashboard_home"),

    # Example for other dashboard routes:
    path("articles/", views.manage_articles, name="manage_articles"),
    path("articles/add/", views.add_article, name="add_article"),
    path("articles/edit/<int:pk>/", views.edit_article, name="edit_article"),
    path("articles/delete/<int:pk>/", views.delete_article, name="delete_article"),

    path("comments/", views.manage_comments, name="manage_comments"),
    path("comments/delete/<int:pk>/", views.delete_comment, name="delete_comment"),

    path("breaking-news/", views.manage_breaking_news, name="manage_breaking_news"),
    path("breaking-news/add/", views.add_breaking_news, name="add_breaking_news"),
    path("breaking-news/edit/<int:pk>/", views.edit_breaking_news, name="edit_breaking_news"),
    path("breaking-news/delete/<int:pk>/", views.delete_breaking_news, name="delete_breaking_news"),

    path("analytics/", views.analytics_view, name="analytics"),
]

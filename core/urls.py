from django.urls import path
from . import views

app_name = "core"  # namespace matches your navbar

urlpatterns = [
    # Home / Article list
    path("", views.home_view, name="home"),  # homepage lists articles

    path("dashboard/", views.dashboard_home, name="dashboard_home"),


    # Article detail by slug
    path("article/<slug:slug>/", views.article_detail, name="article_detail"),

    # Breaking news list & detail
    path("breaking-news/", views.breaking_news_list, name="breaking_news_list"),
    path("breaking-news/<slug:slug>/", views.breaking_news_detail, name="breaking_news_detail"),

    # Categories & Tags
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
    path("tag/<slug:slug>/", views.tag_detail, name="tag_detail"),
]

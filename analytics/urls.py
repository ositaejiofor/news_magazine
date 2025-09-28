from django.urls import path
from . import views

app_name = "analytics"

urlpatterns = [
    # Analytics home
    path("", views.analytics_home, name="analytics_home"),

    # Example analytics pages
    path("traffic/", views.traffic_report, name="traffic_report"),
    path("user-stats/", views.user_stats, name="user_stats"),
    path("engagement/", views.engagement_report, name="engagement_report"),
]

# news_magazine/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from donate import views
from news import views as news_views


def health_check(request):
    """Simple health check endpoint for monitoring."""
    return JsonResponse({"status": "ok"})


urlpatterns = [
    # Health check
    path("health/", health_check, name="health_check"),

    # Admin
    path("admin/", admin.site.urls),

    # Home page
    path("", news_views.home_view, name="home"),

    # Core
    path("core/", include(("core.urls", "core"), namespace="core")),

    # News
    path("news/", include(("news.urls", "news"), namespace="news")),

    # Ads
    path("ads/", include(("ads.urls", "ads"), namespace="ads")),

    # Dashboard
    path("dashboard/", include(("dashboard.urls", "dashboard"), namespace="dashboard")),

    # Accounts (custom app)
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),

    # Django built-in authentication (login, logout, password reset, etc.)
    path("auth/", include("django.contrib.auth.urls")),

    # Subscriptions
    path("subscriptions/", include(("subscriptions.urls", "subscriptions"), namespace="subscriptions")),

    # Analytics
    path("analytics/", include(("analytics.urls", "analytics"), namespace="analytics")),

    path("donate/", include("donate.urls")),

    # Notifications
    path("notifications/", include(("notifications.urls", "notifications"), namespace="notifications")),

    # CKEditor (media uploads)
    path("ckeditor/", include("ckeditor_uploader.urls")),

    # Favicon
    path("favicon.ico", RedirectView.as_view(url=settings.STATIC_URL + "images/favicon.ico")),
]

# Static & Media files (development only)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

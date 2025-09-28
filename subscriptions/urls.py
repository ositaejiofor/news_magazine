# subscriptions/urls.py
from django.urls import path
from . import views

app_name = "subscriptions"

urlpatterns = [
    # Subscribe page (create or update a subscription)
    path("subscribe/", views.subscribe, name="subscribe"),

    # Success page (shown after subscribing)
    path("success/", views.subscription_success, name="success"),

    # Subscription dashboard/home (/subscriptions/)
    path("", views.subscription_home, name="home"),
]

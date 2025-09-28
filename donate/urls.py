from django.urls import path
from . import views


urlpatterns = [
    path("", views.donate_view, name="donate"),
    path("create-checkout-session/", views.create_checkout_session, name="create_checkout_session"),
    path("webhook/", views.stripe_webhook, name="stripe_webhook"),
]

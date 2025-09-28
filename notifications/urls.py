from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path("", views.notification_list, name="home"),
    path("mark-read/<int:pk>/", views.mark_as_read, name="mark_as_read"),
    path("delete/<int:pk>/", views.delete_notification, name="delete"),
]

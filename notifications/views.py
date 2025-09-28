from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Notification

def notification_list(request):
    notifications = Notification.objects.all().order_by("-created_at")
    return render(request, "notifications/notification_list.html", {"notifications": notifications})

def mark_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    notification.is_read = True
    notification.save()
    messages.success(request, "Notification marked as read.")
    return redirect("notifications:home")

def delete_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    notification.delete()
    messages.success(request, "Notification deleted.")
    return redirect("notifications:home")

# subscriptions/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Subscription


@login_required
def subscribe(request):
    """
    Handle subscription form submission.
    - POST: create or update a subscription for the logged-in user.
    - GET: render the subscription form.
    """
    if request.method == "POST":
        email = request.POST.get("email")
        plan = request.POST.get("plan")

        if not email:
            messages.error(request, "Please provide an email address.")
            return redirect("subscriptions:subscribe")

        # Get or create subscription for this user
        subscription, created = Subscription.objects.get_or_create(
            user=request.user,
            email=email,
            defaults={"active": True, "plan": plan or "free"},
        )

        if not created:
            subscription.plan = plan or subscription.plan
            if not subscription.active:
                subscription.active = True
                messages.success(request, "Your subscription has been re-activated.")
            else:
                messages.info(request, "Your subscription was updated.")
            subscription.save()
        else:
            messages.success(request, "You have successfully subscribed.")

        # ✅ Redirect to subscription home instead of reload
        return redirect("subscriptions:home")

    return render(request, "subscriptions/subscribe.html")


@login_required
def subscription_success(request):
    """
    Show success page after subscribing (optional).
    """
    return render(request, "subscriptions/subscription_success.html")


@login_required
def subscription_home(request):
    """
    Show subscription dashboard/homepage for the user.
    """
    subscription = Subscription.objects.filter(user=request.user).first()
    return render(
        request,
        "subscriptions/subscription_home.html",
        {"subscription": subscription},
    )

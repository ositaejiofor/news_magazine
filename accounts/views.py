# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.conf import settings
from .forms import RegisterForm, ProfileUpdateForm, CustomPasswordChangeForm
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect


# --------------------------------------------------
# REGISTER
def register_view(request):
    """
    Handles user registration.
    Superusers are redirected to the dashboard.
    Normal users are redirected to profile page.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration

            if user.is_superuser:
                return redirect('dashboard:dashboard_home')
            else:
                return redirect('accounts:profile')
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


# ---------------------------
# LOGIN VIEW
# ---------------------------
def login_view(request):
    """
    Handles user login.
    Superusers are redirected to the dashboard.
    Normal users are redirected to profile page.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect('dashboard:dashboard_home')
            else:
                return redirect('accounts:profile')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")


# ---------------------------
# LOGOUT VIEW
# ---------------------------
@login_required
def logout_view(request):
    """
    Logs out any authenticated user and redirects to home page.
    """
    logout(request)
    return redirect('core:home')


# ---------------------------
# PROFILE VIEW (optional)
# ---------------------------
@login_required
def profile_view(request):
    """
    Simple profile page for logged-in users.
    """
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "accounts/profile.html", {"form": form})

# --------------------------------------------------
# CHANGE PASSWORD
# --------------------------------------------------
@login_required
def change_password_view(request):
    """
    Allows logged-in users to change their password.
    """
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep logged in after password change
            messages.success(request, "Password updated successfully.")
            return redirect("accounts:profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, "accounts/change_password.html", {"form": form})

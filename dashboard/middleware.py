from django.shortcuts import redirect
from django.urls import reverse

class StaffRequiredMiddleware:
    """
    Ensures that only staff members (is_staff=True) can access /dashboard/.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Restrict only dashboard routes
        if request.path.startswith("/dashboard/") and not request.user.is_staff:
            return redirect(f"{reverse('login')}?next={request.path}")
        return self.get_response(request)

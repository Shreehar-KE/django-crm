from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse


class ApprovalRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.username != settings.ADMIN_NAME:
            if not request.user.is_approved and request.path not in [
                reverse("accounts:approval_status"),
                reverse("analytics:live-users"),
                reverse("analytics:get-likes-count"),
                reverse("analytics:like"),
                reverse("account_logout"),
            ]:
                return redirect("accounts:approval_status")
        return self.get_response(request)

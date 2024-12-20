from datetime import timedelta

from django.contrib.sessions.models import Session
from django.urls import reverse
from django.utils.timezone import now


class LiveUsersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in [
            reverse("analytics:live-users"),
        ]:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()

            self.update_session_activity(request, request.session.session_key)

        response = self.get_response(request)
        return response

    def update_session_activity(self, request, session_key):
        try:
            session = Session.objects.get(session_key=session_key)
            session.expire_date = now() + timedelta(
                seconds=request.session.get_expiry_age()
            )
            print(f"Session Updated: Key={session_key}, Expiry={session.expire_date}")
        except Session.DoesNotExist:
            print(f"Session Does Not Exist: Key={session_key}")

    @staticmethod
    def get_active_user_count():
        sessions = Session.objects.filter(expire_date__gte=now())
        return sessions.count()

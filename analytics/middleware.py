from django.contrib.sessions.models import Session
from django.utils.timezone import now
from datetime import timedelta


class ActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        session_key = request.session.session_key
        if not session_key:
            request.session.create()

        self.update_session_activity(request, request.session.session_key)

        response = self.get_response(request)
        return response

    def update_session_activity(self, request, session_key):
        try:
            session = Session.objects.get(
                session_key=session_key)
            session.expire_date = now() + timedelta(request.session.get_expiry_age())
            session.save()
        except Session.DoesNotExist:
            pass

    @staticmethod
    def get_active_user_count():
        # Query active sessions (non-expired)
        sessions = Session.objects.filter(expire_date__gte=now())
        return sessions.count()

from django.contrib import admin
from django.views.generic import TemplateView
from django.http import HttpResponseServerError
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


def trigger_server_error(request):
    # Raise a 500 Internal Server Error explicitly
    return HttpResponseServerError()


urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("analytics/", include("analytics.urls")),
    path("error/", trigger_server_error, name="server-error"),
]

if settings.MAINTENANCE:
    urlpatterns += [
        path("", TemplateView.as_view(template_name="maintenance.html"), name="maintenance")
    ]
else:
    urlpatterns += [
        path("accounts/", include("allauth.urls")),
        path("accounts/", include("accounts.urls")),
        path("", include("a_contacts.urls")),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

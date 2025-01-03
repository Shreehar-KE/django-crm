from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("analytics/", include("analytics.urls")),
]

if settings.MAINTENANCE:
    urlpatterns += [
        path(
            "",
            TemplateView.as_view(template_name="maintenance.html"),
            name="maintenance",
        )
    ]
else:
    urlpatterns += [
        path("accounts/", include("allauth.urls")),
        path("", include("accounts.urls")),
        path("", include("a_contacts.urls")),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

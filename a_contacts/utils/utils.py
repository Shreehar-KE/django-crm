from django.shortcuts import get_object_or_404
from django.http import Http404


def get_active_object_or_404(cls, *args, **kwargs):
    queryset = cls.objects.all() if hasattr(cls, "_default_manager") else cls
    queryset = queryset.filter(deleted_at__isnull=True)

    return get_object_or_404(queryset, *args, **kwargs)

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Like


def like_view(request):
    ip = get_client_ip(request)
    if not Like.objects.filter(ip_address=ip).exists():
        Like.objects.create(ip_address=ip)
    likes_count = Like.objects.count()
    return HttpResponse(likes_count)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def live_users_view(request):
    # logic for counting live_logged_in_users
    return HttpResponse(5)
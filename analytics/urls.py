from django.urls import path

from . import views

app_name = "analytics"
urlpatterns = [
    path("like/", views.like_view, name="like"),
    path("likescount/", views.get_likes_count_view, name="get-likes-count"),
    path("liveusers/", views.live_users_view, name="live-users"),
]

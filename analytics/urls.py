from django.urls import path
from .views import like_view

app_name = 'analytics'
urlpatterns = [
    path('like/', like_view, name='like'),
]

from django.urls import path
from . import views
app_name = 'a_contacts'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home')
]

from django.urls import path
from . import views
app_name = 'a_customers'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home')
]



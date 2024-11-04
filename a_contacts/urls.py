from django.urls import path
from . import views
app_name = 'a_contacts'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('contact/create/', views.ContactCreateView.as_view(),
         name='contact-create'),
    path('contact/<uuid:pk>/update', views.ContactUpdateView.as_view(),
         name='contact-update'),

]

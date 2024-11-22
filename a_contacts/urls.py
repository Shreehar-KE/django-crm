from django.urls import path
from . import views
app_name = 'a_contacts'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('contact/create/', views.ContactCreateView.as_view(),
         name='contact-create'),
    path('contact/bulkcreate/', views.contactBulkCreateView,
         name='contact-bulk-create'),
    path('contact/bulkcreate/preview/', views.contactBulkCreatePreview, name='contact-bulk-create-preview'),
    path('contact/<uuid:pk>/', views.ContactDetailView.as_view(),
         name='contact-detail'),
    path('contact/<uuid:pk>/update/', views.ContactUpdateView.as_view(),
         name='contact-update'),
    path('contact/<uuid:pk>/delete/', views.contactDeleteView,
         name='contact-delete'),
    path('contact/create/fake/', views.fillContactForm,
         name='fake-contact-create'),
    path('contact/bulkcreate/fake/',views.exportRandomDataCSV, name='fake-csv-data')
]

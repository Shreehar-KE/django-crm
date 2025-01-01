from django.contrib import admin
from .models import Contact, ContactIDCounter

admin.site.register(Contact)
admin.site.register(ContactIDCounter)

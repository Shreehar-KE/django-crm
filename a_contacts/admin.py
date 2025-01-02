from django.contrib import admin

from .models import Contact, ContactIDCounter, Event

admin.site.register(Contact)
admin.site.register(ContactIDCounter)
admin.site.register(Event)

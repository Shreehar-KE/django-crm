from django.contrib import admin

from .models import Contact, ContactIDCounter, Event



class ContactAdmin(admin.ModelAdmin):
    list_filter = ("deleted_at",)
    actions = ["restore_contacts"]

    def restore_contacts(self, request, queryset):
        for contact in queryset:
            contact.updated_by = request.user
            contact.restore()

    restore_contacts.short_description = "Restore selected contacts"

admin.site.register(Contact, ContactAdmin)

admin.site.register(ContactIDCounter)
admin.site.register(Event)

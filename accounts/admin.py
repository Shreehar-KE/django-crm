from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = [
        "username",
        "email",
        "approval_status",
        "role",
        "employee_id",
    ]
    list_filter = UserAdmin.list_filter + ("approval_status",)
    actions = ["approve_users"]
    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {
                "fields": (
                    "approval_status",
                    "is_approved",
                    "image",
                    "location",
                    "role",
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": (
                    "email",
                    "approval_status",
                )
            },
        ),
    )

    def approve_users(self, request, queryset):
        queryset.update(approval_status="approved")

    approve_users.short_description = "Approve selected users"

admin.site.register(CustomUser, CustomUserAdmin)

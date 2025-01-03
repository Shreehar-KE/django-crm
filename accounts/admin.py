from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = get_user_model()
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
        for user in queryset:
            user.approval_status = "approved"
            user.is_approved = True
            user.save()

    approve_users.short_description = "Approve selected users"


admin.site.register(get_user_model(), CustomUserAdmin)

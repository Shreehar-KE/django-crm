from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = [
        "email",
        "username",
        "is_approved",
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("is_approved",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {
                "fields": (
                    "email",
                    "is_approved",
                )
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)

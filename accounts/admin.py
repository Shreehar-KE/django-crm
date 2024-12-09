from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        'email',
        'username',
        'is_approved',
    ]
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('is_approved',)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields': ('is_approved',)}),)

admin.site.register(CustomUser, CustomUserAdmin)

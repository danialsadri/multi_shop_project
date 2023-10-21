from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ["phone_number", "email", "full_name", "is_admin"]
    list_filter = ["is_admin"]
    search_fields = ["phone_number", "email"]
    ordering = ["email"]
    readonly_fields = ['last_login']
    filter_horizontal = ['groups', 'user_permissions']

    fieldsets = [
        (None, {"fields": ["phone_number", "password"]}),
        ("Personal info", {"fields": ["email", "full_name"]}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_superuser', 'last_login', 'groups', 'user_permissions')}),
    ]
    add_fieldsets = [
        (None, {"classes": ["wide"], "fields": ["phone_number", "password1", "password2"]}),
    ]

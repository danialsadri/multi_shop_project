from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Otp, Address, ContactUs
from .forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _

admin.sites.AdminSite.site_title = _('control panel')
admin.sites.AdminSite.site_header = _('control panel')
admin.sites.AdminSite.index_title = _('control panel')


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
        (_("Personal info"), {"fields": ["email", "full_name"]}),
        (_('Permissions'),
         {'fields': ('is_active', 'is_admin', 'is_superuser', 'last_login', 'groups', 'user_permissions')}),
    ]
    add_fieldsets = [
        (None, {"classes": ["wide"], "fields": ["phone_number", "password1", "password2"]}),
    ]


@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ['phone', 'code', 'expiration_date']
    list_filter = ['expiration_date']
    search_fields = ['phone']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'email', 'phone', 'postal_code']
    list_filter = ['user']
    search_fields = ['full_name', 'email', 'phone']
    raw_id_fields = ['user']


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'subject']
    list_filter = ['subject']
    search_fields = ['name', 'subject']

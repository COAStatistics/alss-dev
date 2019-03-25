from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from apps.users.models import User
from apps.users.forms import UserChangeForm, UserCreationForm


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ['full_name', 'email', 'mobile', 'is_staff', 'is_superuser']
    fieldsets = [
        [_('Auth'), {'fields': ['email', 'mobile', 'password']}],
        [_('Personal info'), {'fields': ['full_name']}],
        [_('Settings'), {'fields': ['groups', 'is_active', 'is_staff', 'is_superuser']}],
        [_('Important dates'), {'fields': ['last_login', 'registered_at']}],
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        [None, {'classes': ['wide'],
                'fields': ['email', 'full_name', 'password1', 'password2']}],
    ]
    search_fields = ['email']
    ordering = ['email']
    readonly_fields = ['is_superuser', 'last_login', 'registered_at']


admin.site.register(User, UserAdmin)

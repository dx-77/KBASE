from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from main.models import Record, Tag, User


class UserProfileAdmin(UserAdmin):
    model = User

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            _('Персональная информация'),
            {'fields': ('user_type', 'first_name', 'last_name', 'email')}
        ),
        # (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',)}),
        (_('Даты'), {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('username', 'user_type', 'email', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'phone',)
    list_filter = ()


admin.site.register(Record)
admin.site.register(Tag)
admin.site.register(User, UserProfileAdmin)

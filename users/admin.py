from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Profile, ListColShow, PunchCard, AccountVar

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(ListColShow)
admin.site.register(PunchCard)
admin.site.register(AccountVar)


class UserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)

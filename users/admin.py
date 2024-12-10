from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, PasswordReset



class UserAdmin(BaseUserAdmin):
    ordering = ('email',)
    list_display = ('email', 'is_staff', 'is_active')
    search_fields = ('email',)
    readonly_fields = ('id',)

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
    
    
    
admin.site.register(User)
admin.site.register(PasswordReset)
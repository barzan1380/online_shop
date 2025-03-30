from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .decorators import admin_required
from django.shortcuts import render
from .decorators import admin_required


# Register your models here.

class CustomUserAdin(UserAdmin):
    list_display = ('phone', 'role', 'is_active',)
    list_filter = ('is_active', 'role')
    list_editable = ('is_active', 'role')
    search_fields = ('phone', 'role')
    ordering = ('role',)
    fieldsets = (
        (None, {"fields": ('phone', 'password')}),
        ("اطلاعات شخصی", {"fields": ('first_name', 'last_name', 'address')}),
        ("دسترسی ها", {"fields": ('is_active', 'is_staff', 'is_superuser')}),
        ("نقش کاربر", {"fields": ('role',)}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone", 'password1', 'password2', 'role'),
        }),
    )


# @admin_required
# def admin_dashboard(request):
#     return render(request, 'account/admin_dashboard.html')


admin.site.register(CustomUser, CustomUserAdin)

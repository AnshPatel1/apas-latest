from django.contrib import admin
from .models import *
from django import forms


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'designation', 'department', 'school', 'roles']
    list_filter = ['designation', 'department', 'school', 'roles', 'is_staff', 'is_admin', 'is_ro1', 'is_ro2', 'is_hr', "is_hod"]
    search_fields = ['full_name', 'username', 'email', 'designation', 'department', 'school', 'roles', 'is_staff', 'is_admin',
                     'is_ro1', 'is_ro2', 'is_hr', 'is_hod']
    # filter_horizontal = ['permissions_mixin']
    list_per_page = 25
    filter_horizontal = ['user_permissions']
    exclude = ('password',)
    # add search for foreign field ro1_id, ro2_id
    # code starts below
    autocomplete_fields = ['ro1_id', 'ro2_id']
    # filter_horizontal = ['permissions_mixin']


class DualRoleAdmin(admin.ModelAdmin):
    autocomplete_fields = ['main_user', 'faculty_profile']


admin.site.register(User, UserAdmin)
admin.site.register(PasswordReset)
admin.site.register(DualRole, DualRoleAdmin)

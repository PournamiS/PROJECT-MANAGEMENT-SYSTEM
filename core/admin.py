from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Project, Task


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display  = ['username', 'email', 'role', 'is_active']
    list_filter   = ['role']
    fieldsets     = UserAdmin.fieldsets + (('Role', {'fields': ('role',)}),)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display     = ['name', 'created_by', 'created_at']
    filter_horizontal = ['members']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'assigned_to', 'status', 'created_at']
    list_filter  = ['status', 'project']

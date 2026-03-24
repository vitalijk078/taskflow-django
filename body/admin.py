from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Role, Task, TaskCategory, User


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Дополнительно", {"fields": ("full_name", "login", "role")}),)
    list_display = ("username", "full_name", "email", "role", "is_staff")
    search_fields = ("username", "full_name", "email")


@admin.register(TaskCategory)
class TaskCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "status", "priority", "due_date", "is_completed")
    list_filter = ("status", "priority", "category", "is_completed")
    search_fields = ("title", "description", "user__username", "user__full_name")

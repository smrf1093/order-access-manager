from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_staff", "is_active")
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("role",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("role",)}),)
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "email")

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "role":
            kwargs["choices"] = [
                ("CUSTOMER", "Customer"),
                ("ADMIN", "Admin"),
            ]
        return super().formfield_for_choice_field(db_field, request, **kwargs)

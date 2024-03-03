from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """
    Define Admin Model for custom User Model with no email field:
        - Extending original Django UserAdmin class
        - Replacing username for email
        - Registering new class to Django Admin
    """

    fieldsets = (
        (None, {"fields", ("email", "password")}),
        (_("Personal Info"), {"fields": ("first_name", "last_name")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")})
    )

    add_fields = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
    )

    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)

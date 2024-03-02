from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from typing import Literal

# Customer User Model Manager
class CustomUserManager(BaseUserManager):
    """
    Custom User Manager to replace the Django default username with email
    as the unique identifier for authentication instead of username.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save User with the given email and password
        """
        if not email: raise ValueError("Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Super User is missing is_staff permission")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Super User is missing is_superuser permission")

        return self.create_user(email, password, **extra_fields)


# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model, similar to Django defaut User Mode, except the default "USERNAME_FIELD"
    is set to "email"
    """
    email = models.EmailField(unique = True, null = True)
    first_name = models.CharField(max_length = 30, blank = True)
    last_name = models.CharField(max_length = 30, blank = True)

    # is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(
            _("staff status"),
            default = False,
            help_text = _("Permission whether user can authenticate into the app"),
    )

    is_active = models.BooleanField(
            _("active"),
            default = True,
            help_text = _("Permission whether user is treated as active. Unselect this instead of deleting accounts"),
    )

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email
